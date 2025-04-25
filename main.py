# 📁 github_proxy/main.py
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from fastapi import Query
from pathlib import Path
import httpx, os, json, re
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Optional
import tempfile
import yaml
import requests
import zipfile
from datetime import datetime
import shutil
from copy import deepcopy

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- GitHub File Proxy ----
@app.get("/")
async def root():
    return {"message": "GitHub File Proxy is running."}

# ---- Get file content from GitHub
@app.get("/repos/{owner}/{repo}/contents/{path:path}")
async def get_file(owner: str, repo: str, path: str, ref: str = None):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": ref} if ref else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.text)

# ---- Get multiple files from GitHub ----
@app.post("/batch-files")
async def get_batch_files(request: Request):
    body = await request.json()
    owner = body.get("owner")
    repo = body.get("repo")
    paths = body.get("paths", [])
    ref = body.get("ref")

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    async with httpx.AsyncClient() as client:
        results = []
        for path in paths:
            url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
            params = {"ref": ref} if ref else {}
            resp = await client.get(url, headers=headers, params=params)
            if resp.status_code == 200:
                results.append({"path": path, "content": resp.json()})
            else:
                results.append({"path": path, "error": resp.text})

    return {"files": results}

# --- Task Update Tools ---

# GitHub access settings
GITHUB_REPO = "ai-concussion-agent"
GITHUB_OWNER = "stewmckendry"
TASK_FILE_PATH = "task.yaml"
GITHUB_BRANCH = "main"

class TaskUpdateRequest(BaseModel):
    task_id: str
    fields: Dict[str, str]

def fetch_task_yaml_from_github():
    url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{TASK_FILE_PATH}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Failed to fetch task.yaml from GitHub")
    return yaml.safe_load(response.text)

def fetch_yaml_from_github(file_path: str):
    url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{file_path}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"Failed to fetch {file_path} from GitHub")
    return yaml.safe_load(response.text)

@app.get("/tasks/list")
def list_tasks(
    status: Optional[str] = Query(None),
    pod_owner: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    """
    Return a list of tasks from GitHub task.yaml with optional filters by status, pod_owner, or category.
    """
    try:
        task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task.yaml: {e}")

    tasks = task_data.get("tasks", {})
    filtered_tasks = {}

    for task_id, task in tasks.items():
        if status and task.get("status") != status:
            continue
        if pod_owner and task.get("pod_owner") != pod_owner:
            continue
        if category and task.get("category") != category:
            continue
        filtered_tasks[task_id] = task

    return {"tasks": filtered_tasks}


TASKS_FILE = "task.yaml"
PROMPT_DIR = "prompts/used"

class ActivateTaskRequest(BaseModel):
    task_id: str

@app.post("/tasks/activate")
async def activate_task(request: ActivateTaskRequest):
    
    try:
        task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching task.yaml: {e}")
    
    tasks = task_data.get("tasks", {})
    task_id = request.task_id

    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found")

    # Update task status and timestamp
    tasks[task_id]["status"] = "in_progress"
    tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()

    # Determine prompt file path
    pod = tasks[task_id].get("pod_owner", "unknown")
    prompt_path = f"{PROMPT_DIR}/{pod}/{task_id}_prompt.txt"

    try:
        prompt_content = fetch_yaml_from_github(file_path=prompt_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching prompt file: {e}")

    return {
        "task": tasks[task_id],
        "all_tasks": tasks,
        "status": "in_progress",
        "prompt_path": prompt_path,
        "prompt_content": prompt_content or "Prompt file not found."
    }

class CloneTaskRequest(BaseModel):
    original_task_id: str
    overrides: Optional[Dict[str, str]] = None  # e.g. {"description": "New version of feature"}


@app.post("/tasks/clone")
async def clone_task(request: CloneTaskRequest):
    # Load full task list from GitHub
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    original_task_id = request.original_task_id
    if original_task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Original task ID {original_task_id} not found")

    base_id = original_task_id.split("_")[0]  # e.g. "2.2"
    descriptor = request.descriptor.replace(" ", "_").lower()

    # Find existing variants of the base task ID
    variants = [k for k in tasks.keys() if k.startswith(base_id)]
    suffix = chr(97 + len(variants))  # a, b, c, ...
    new_task_id = f"{base_id}{suffix}_{descriptor}"

    # Create new task metadata
    new_task = deepcopy(tasks[original_task_id])
    new_task.update(request.overrides or {})
    new_task["created_at"] = datetime.utcnow().isoformat()
    new_task["updated_at"] = datetime.utcnow().isoformat()

    # Inject into task list
    tasks[new_task_id] = new_task

    # Retrieve original prompt
    original_pod = tasks[original_task_id].get("pod_owner", "unknown")
    original_prompt_path = f"{PROMPT_DIR}/{original_pod}/{original_task_id}_prompt.txt"
    try:
        original_prompt_content = fetch_yaml_from_github(file_path=original_prompt_path)
    except Exception:
        original_prompt_content = None

    return {
        "message": f"Cloned task as {new_task_id}",
        "new_task_id": new_task_id,
        "new_task_metadata": new_task,
        "updated_tasks": tasks,
        "original_prompt_path": original_prompt_path,
        "original_prompt_content": original_prompt_content
    }

class PromotePatchRequest(BaseModel):
    task_id: str
    summary: str
    output_files: List[str]
    prompt_path: Optional[str] = None  # prompts/used/<pod>/<task_id>_prompt.txt
    reasoning_trace: Optional[str] = None  # Optional free-form reflection text
    output_folder: Optional[str] = "misc"  # Suggest pick-list in prompt: task_updates, dev_outputs, test_outputs, go_live_docs

@app.post("/patches/promote")
async def promote_patch(request: PromotePatchRequest):
    task_id = request.task_id
    summary = request.summary
    output_files = request.output_files
    reasoning_trace = request.reasoning_trace
    prompt_path = request.prompt_path
    output_folder = request.output_folder or "misc"  # Default fallback

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    patch_name = f"patch_{task_id}_{timestamp}.zip"
    zip_folder = f"chatgpt_repo/outputs/{output_folder}"
    zip_path = f"{zip_folder}/{patch_name}"

    os.makedirs(zip_folder, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Save metadata.json
        manifest_path = os.path.join(tmp_dir, "metadata.json")
        with open(manifest_path, "w") as f:
            json.dump({
                "task_id": task_id,
                "summary": summary,
                "output_files": output_files,
                "prompt": prompt_path
            }, f, indent=2)

        # Save reasoning_trace.md
        with open(os.path.join(tmp_dir, "reasoning_trace.md"), "w") as f:
            f.write(reasoning_trace)

        # Copy output files into temp dir, preserving folder structure
        for file_path in output_files:
            dest_path = os.path.join(tmp_dir, file_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as f:
                f.write("PLACEHOLDER: This should be populated by the human lead.")

        # Create ZIP file
        shutil.make_archive(zip_path.replace(".zip", ""), 'zip', tmp_dir)

    return {
        "download_url": zip_path,
        "task_id": task_id,
        "output_folder": output_folder,
        "timestamp": timestamp
    }

@app.get("/tasks/{task_id}")
def get_task_details(task_id: str):
    """
    Return full metadata for a single task from task.yaml
    """
     # Load full task list from GitHub
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found.")

    return {"task_id": task_id, "metadata": tasks[task_id]}  


@app.post("/tasks/create")
def create_new_task(
    phase: str = Body(..., example="Phase2_dev"),
    category: str = Body(..., example="dev"),
    description: str = Body(...),
    pod_owner: str = Body(...),
    inputs: List[str] = Body(default=[]),
    outputs: List[str] = Body(default=[]),
    descriptor: str = Body(..., example="summarize_user_research")
):
    """
    Create a new task from scratch
    """
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    # Generate task_id using next available base index in phase
    base_prefix = get_next_base_id(tasks, phase)
    suffix = "a"
    new_task_id = f"{base_prefix}{suffix}_{descriptor.replace(' ', '_').lower()}"

    # Build prompt path and instance_of
    prompt_path = f"prompts/used/{pod_owner}/{new_task_id}_prompt.txt"
    instance_of = f"task_templates/{phase}/task.yaml"

    new_task = {
        "description": description,
        "phase": phase,
        "category": category,
        "pod_owner": pod_owner,
        "status": "pending",
        "prompt": prompt_path,
        "inputs": inputs,
        "outputs": outputs,
        "ready": True,
        "done": False,
        "created_by": "human",
        "created_at": datetime.utcnow().isoformat(),
        "assigned_to": "unassigned",
        "instance_of": instance_of,
        "updated_at": datetime.utcnow().isoformat()
    }

    tasks[new_task_id] = new_task

    return {
        "message": f"Created new task {new_task_id}",
        "new_task_id": new_task_id,
        "new_task_metadata": new_task,
        "updated_tasks": tasks
    }


def get_next_base_id(tasks, phase):
    phase_index = {
        "Phase1_discovery": "1.",
        "Phase2_dev": "2.",
        "Phase3_test": "3.",
        "Phase4_deploy": "4.",
        "Cross-Phase": "0."
    }.get(phase, "9.")

    # Get max numeric sub-id under this phase
    numbers = [float(t.split("_")[0]) for t in tasks.keys() if t.startswith(phase_index)]
    max_num = max(numbers) if numbers else float(phase_index + "0")
    next_num = round(max_num + 0.1, 1)

    return f"{next_num:.1f}"


# ---- OpenAPI Static File Serving ----

@app.get("/openapi.json")
def serve_openapi():
    with open("openapi.json", "r") as f:
        return JSONResponse(content=json.load(f))

# ✅ Override default FastAPI-generated OpenAPI with static file
from fastapi.openapi.utils import get_openapi

def custom_openapi():
    with open("openapi.json", "r") as f:
        return json.load(f)

app.openapi = custom_openapi
