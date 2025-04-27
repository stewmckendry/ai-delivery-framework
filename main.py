# 📁 github_proxy/main.py

# ---- (1) Imports ----
from fastapi import FastAPI, HTTPException, Request, Body, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
from pathlib import Path
from datetime import datetime
from copy import deepcopy
import httpx
import os
import json
import re
import tempfile
import yaml
import requests
import zipfile
import shutil
import traceback
from github import Github, GithubException
from openai import OpenAI
from dotenv import load_dotenv

# ---- (2) Global Variables ----
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"
GITHUB_REPO = "ai-concussion-agent"
GITHUB_OWNER = "stewmckendry"
TASK_FILE_PATH = "task.yaml"
GITHUB_BRANCH = "main"
PROMPT_DIR = "prompts/used"
MEMORY_FILE_PATH = "memory.yaml"
REASONING_FOLDER_PATH = ".logs/reasoning/"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- (3) Classes ----
class TaskUpdateRequest(BaseModel):
    task_id: str
    fields: Dict[str, str]

class ActivateTaskRequest(BaseModel):
    task_id: str

class CloneTaskRequest(BaseModel):
    original_task_id: str
    overrides: Optional[Dict[str, str]] = None  # e.g. {"description": "New version of feature"}

class TaskMetadataUpdate(BaseModel):
    description: Optional[str] = None
    prompt: Optional[str] = None
    inputs: Optional[List[str]] = None
    outputs: Optional[List[str]] = None
    ready: Optional[bool] = None
    done: Optional[bool] = None

class PromotePatchRequest(BaseModel):
    task_id: str
    summary: str
    output_files: Dict[str, str]  # filename -> content mapping
    reasoning_trace: str
    prompt_path: Optional[str] = None
    output_folder: Optional[str] = None
    handoff_notes: Optional[str] = None  # <<< NEW

class MemoryFileEntry(BaseModel):
    file_path: str
    description: str
    tags: List[str]

class AddToMemoryRequest(BaseModel):
    files: List[MemoryFileEntry]

# ---- (4) Helper Functions ----
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

def fetch_file_content_from_github(file_path: str):
    url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{GITHUB_BRANCH}/{file_path}"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail=f"Failed to fetch {file_path} from GitHub")
    return response.text

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

def list_files_from_github(path):
    url = f"{GITHUB_API}/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    # Handle if it's a single file vs directory
    if isinstance(data, dict):
        return [data]
    return [item for item in data if item["type"] == "file"]

def generate_metrics_summary():
    task_data = fetch_yaml_from_github(TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks.values() if t.get("done", False))

    # Cycle time
    cycle_times = []
    for t in tasks.values():
        if t.get("done") and t.get("created_at") and t.get("updated_at"):
            created = datetime.fromisoformat(t["created_at"])
            updated = datetime.fromisoformat(t["updated_at"])
            cycle_times.append((updated - created).total_seconds() / (3600 * 24))  # days

    avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else None

    # Reasoning logs
    scores = []
    recalls = 0
    novelties = 0
    total_logs = 0

    reasoning_files = list_files_from_github(REASONING_FOLDER_PATH)
    for file in reasoning_files:
        filename = file["name"]
        if filename.endswith(".md") and not filename.endswith("_summary.md"):
            contents = fetch_file_content_from_github(REASONING_FOLDER_PATH + filename)
            if "Thought Quality Score:" in contents:
                score_line = contents.split("Thought Quality Score:")[1].splitlines()[0]
                score = int(score_line.strip())
                scores.append(score)
            if "[recall_used]" in contents or "Recall Used: yes" in contents:
                recalls += 1
            if "[novel_insight]" in contents or "Novel Insight: yes" in contents:
                novelties += 1
            total_logs += 1

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "quantitative": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate_percent": (completed_tasks / total_tasks * 100) if total_tasks else 0,
            "average_cycle_time_days": avg_cycle_time,
            "patch_success_rate_percent": None  # Future
        },
        "qualitative": {
            "average_thought_quality_score": (sum(scores) / len(scores)) if scores else None,
            "recall_usage_percent": (recalls / total_logs * 100) if total_logs else 0,
            "novelty_rate_percent": (novelties / total_logs * 100) if total_logs else 0
        }
    }

def generate_project_reasoning_summary():
    reasoning_files = list_files_from_github(REASONING_FOLDER_PATH)
    all_thoughts = []

    for file in reasoning_files:
        filename = file["name"]
        if filename.endswith(".md") and not filename.endswith("_summary.md"):
            contents = fetch_file_content_from_github(REASONING_FOLDER_PATH + filename)
            if "## Thoughts" in contents:
                thoughts_section = contents.split("## Thoughts")[1]
                all_thoughts.append(thoughts_section)

    merged_thoughts = "\n".join(all_thoughts)

    prompt = f"""
You are summarizing the collective reasoning across multiple AI tasks.

Here are the collected reasoning thoughts:

{merged_thoughts}

Please summarize:
- Main reasoning themes across tasks
- Key insights discovered
- Common patterns of memory reuse (recall)
- Novel ideas that emerged
- General quality of the AI reasoning

Keep your summary under 250 words.
"""

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    project_summary = response.choices[0].message.content.strip()
    return project_summary

# ---- (5) API Routes ----

# ---- Root ----
@app.get("/")
async def root():
    return {"message": "GitHub File Proxy is running."}

# ---- GitHub File Proxy ----
@app.get("/repos/{owner}/{repo}/contents/{path:path}")
async def get_file(owner: str, repo: str, path: str, ref: str = None):
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }
    url = f"{GITHUB_API}/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": ref} if ref else {}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params, headers=headers)
            response.raise_for_status()
            data = await response.json()  # <-- critical: await here
            return data
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"{await e.response.aread()}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

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

# ---- Task Management ----
@app.get("/tasks/list")
def list_tasks(
    status: Optional[str] = Query(None),
    pod_owner: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
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

    tasks[task_id]["status"] = "in_progress"
    tasks[task_id]["updated_at"] = datetime.utcnow().isoformat()

    pod = tasks[task_id].get("pod_owner", "unknown")
    prompt_path = f"{PROMPT_DIR}/{pod}/{task_id}_prompt.txt"

    try:
        prompt_content = fetch_yaml_from_github(file_path=prompt_path)
    except Exception as e:
        prompt_content = None

    if prompt_content is None:
        prompt_content = "Prompt file not found. Please auto-generate it."

    return {
        "task": tasks[task_id],
        "all_tasks": tasks,
        "status": "in_progress",
        "prompt_path": prompt_path,
        "prompt_content": prompt_content
    }

@app.post("/tasks/clone")
async def clone_task(request: CloneTaskRequest):
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    original_task_id = request.original_task_id
    if original_task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Original task ID {original_task_id} not found")

    base_id = original_task_id.split("_")[0]
    descriptor = request.descriptor.replace(" ", "_").lower()

    variants = [k for k in tasks.keys() if k.startswith(base_id)]
    suffix = chr(97 + len(variants))
    new_task_id = f"{base_id}{suffix}_{descriptor}"

    new_task = deepcopy(tasks[original_task_id])
    new_task.update(request.overrides or {})
    new_task["created_at"] = datetime.utcnow().isoformat()
    new_task["updated_at"] = datetime.utcnow().isoformat()

    tasks[new_task_id] = new_task

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

@app.post("/patches/promote")
async def promote_patch(request: PromotePatchRequest):
    task_id = request.task_id
    summary = request.summary
    output_files = request.output_files
    reasoning_trace = request.reasoning_trace
    prompt_path = request.prompt_path
    output_folder = request.output_folder or "misc"
    handoff_notes = request.handoff_notes  # <<< NEW

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    patch_name = f"patch_{task_id}_{timestamp}.zip"
    zip_folder = f"chatgpt_repo/outputs/{output_folder}"
    zip_path = f"{zip_folder}/{patch_name}"

    os.makedirs(zip_folder, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp_dir:
        manifest_path = os.path.join(tmp_dir, "metadata.json")
        with open(manifest_path, "w") as f:
            json.dump({
                "task_id": task_id,
                "summary": summary,
                "output_files": output_files,
                "prompt": prompt_path
            }, f, indent=2)

        with open(os.path.join(tmp_dir, "reasoning_trace.md"), "w") as f:
            f.write(reasoning_trace)

        for file_path, file_content in output_files.items():
            dest_path = os.path.join(tmp_dir, file_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w") as f:
                f.write(file_content)
        
        # Optionally write handoff notes
        if handoff_notes:
            handoff_dir = os.path.join(tmp_dir, "handoff_notes")
            os.makedirs(handoff_dir, exist_ok=True)
            with open(os.path.join(handoff_dir, f"{task_id}_handoff.md"), "w") as f:
                f.write(handoff_notes)
                
        # Fetch latest memory.yaml from GitHub
        try:
            memory = fetch_yaml_from_github(file_path=MEMORY_FILE_PATH)
        except Exception:
            memory = {}

        def smart_merge_memory(memory, key, file_path, description, tags):
            existing_entry = memory.get(key)
            if existing_entry:
                # Merge description if not already meaningful
                if existing_entry.get("description", "").startswith("Output file generated from task") or not existing_entry.get("description"):
                    existing_entry["description"] = description
                # Merge tags (union)
                existing_tags = set(existing_entry.get("tags", []))
                new_tags = set(tags)
                existing_entry["tags"] = list(existing_tags.union(new_tags))
                existing_entry["last_updated"] = timestamp
            else:
                memory[key] = {
                    "file_path": file_path,
                    "description": description,
                    "tags": tags,
                    "last_updated": timestamp
                }

        # --- Add files to memory ---

        # 1. Output files
        for file_path in output_files.keys():
            key = file_path.replace("/", "_").replace(".", "_")
            smart_merge_memory(memory, key, file_path, f"Output file generated from task {task_id}", ["project", "outputs"])

        # 2. Reasoning trace
        trace_key = f"logs_reasoning_{task_id}_reasoning_trace_md"
        smart_merge_memory(memory, trace_key, f".logs/reasoning/{task_id}_reasoning_trace.md", f"Reasoning trace for task {task_id}", ["project", "reasoning"])

        # 3. Prompt used
        if prompt_path:
            prompt_key = prompt_path.replace("/", "_").replace(".", "_")
            smart_merge_memory(memory, prompt_key, prompt_path, f"Prompt used for task {task_id}", ["project", "prompt"])

        # Save updated memory.yaml into tmp_dir
        memory_path = os.path.join(tmp_dir, "memory.yaml")
        with open(memory_path, "w") as f:
            yaml.safe_dump(memory, f, sort_keys=False)

        shutil.make_archive(zip_path.replace(".zip", ""), 'zip', tmp_dir)

    return {
        "download_url": zip_path,
        "task_id": task_id,
        "output_folder": output_folder,
        "timestamp": timestamp
    }

@app.get("/tasks/{task_id}")
def get_task_details(task_id: str):
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
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    base_prefix = get_next_base_id(tasks, phase)
    suffix = "a"
    new_task_id = f"{base_prefix}{suffix}_{descriptor.replace(' ', '_').lower()}"

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


@app.patch("/tasks/update_metadata/{task_id}")
def update_task_metadata(
    task_id: str,
    description: Optional[str] = Body(None),
    prompt: Optional[str] = Body(None),
    inputs: Optional[List[str]] = Body(default=None),
    outputs: Optional[List[str]] = Body(default=None),
    ready: Optional[bool] = Body(default=None),
    done: Optional[bool] = Body(default=None)
):
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task ID not found.")

    task = tasks[task_id]

    # Apply updates if provided
    if description is not None:
        task["description"] = description
    if prompt is not None:
        task["prompt"] = prompt
    if inputs is not None:
        task["inputs"] = inputs
    if outputs is not None:
        task["outputs"] = outputs
    if ready is not None:
        task["ready"] = ready
    if done is not None:
        task["done"] = done

    # Always update the updated_at timestamp
    task["updated_at"] = datetime.utcnow().isoformat()

    return {
        "message": f"Updated metadata for task {task_id}",
        "task_id": task_id,
        "updated_task_metadata": task,
        "updated_tasks": tasks
    }


# ---- Memory Management ----

@app.post("/memory/index")
def index_memory(
    base_paths: List[str] = Body(default=[
        "prompts/",
        "scripts/",
        "task_templates/",
        "main.py",
        "openapi.json"
    ])
):
    memory = {}

    for path in base_paths:
        file_list = list_files_from_github(path)
        for file_info in file_list:
            file_path = file_info["path"]
            key = file_path.replace("/", "_").replace(".", "_")
            memory[key] = {
                "file_path": file_path,
                "description": "To be filled manually or later",
                "tags": ["framework"]
            }

    try:
        existing_memory = fetch_yaml_from_github(file_path=MEMORY_FILE_PATH)
        existing_memory.update(memory)
    except Exception:
        existing_memory = memory

    return {
        "message": f"Indexed {len(memory)} files into memory.yaml",
        "memory_index": existing_memory
    }


@app.post("/memory/diff")
def memory_diff(
    base_paths: List[str] = Body(default=[
        "prompts/",
        "scripts/",
        "task_templates/",
        "main.py",
        "openapi.json"
    ])
):
    """
    Compare GitHub repo file list with memory.yaml and return missing files
    """
    missing_files = []
    
    # Fetch current memory.yaml
    try:
        memory = fetch_yaml_from_github(file_path=MEMORY_FILE_PATH)
    except Exception:
        memory = {}

    memory_paths = {v["file_path"] for v in memory.values()}

    # Scan GitHub using updated direct GitHub call
    for path in base_paths:
        file_list = list_files_from_github(path)
        for file_info in file_list:
            file_path = file_info["path"]
            if file_path not in memory_paths:
                missing_files.append(file_path)

    return {
        "message": f"Found {len(missing_files)} missing files",
        "missing_files": missing_files
    }

@app.post("/memory/add")
def add_to_memory(request: AddToMemoryRequest):
    """
    Add new files with metadata to memory.yaml
    """
    try:
        memory = fetch_yaml_from_github(file_path=MEMORY_FILE_PATH)
    except Exception:
        memory = {}

    for file_entry in request.files:
        key = file_entry.file_path.replace("/", "_").replace(".", "_")
        memory[key] = {
            "file_path": file_entry.file_path,
            "description": file_entry.description,
            "tags": file_entry.tags
        }

    return {
        "message": f"Added {len(request.files)} files to memory index",
        "memory_index": memory
    }

@app.post("/memory/validate-files")
def validate_memory_file_exists(files: List[str] = Body(...)):
    """
    Validate if the given files exist in memory.yaml and/or GitHub repo.
    """
    try:
        memory = fetch_yaml_from_github(file_path=MEMORY_FILE_PATH)
    except Exception:
        memory = {}

    results = []

    for file_path in files:
        memory_match = any(entry.get("file_path") == file_path for entry in memory.values())
        github_match = False

        # Try GitHub lookup (optional lightweight HEAD check)
        github_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/contents/{file_path}"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        try:
            response = requests.head(github_url, headers=headers)
            github_match = response.status_code == 200
        except Exception:
            github_match = False

        results.append({
            "file_path": file_path,
            "exists_in_memory": memory_match,
            "exists_in_github": github_match
        })

    return {
        "validated_files": results
    }


@app.get("/memory/search")
def search_memory(keyword: str):
    """
    Search memory.yaml for files matching keyword in file_path, description, or tags
    """
    try:
        memory = fetch_yaml_from_github(file_path=MEMORY_FILE_PATH)
    except Exception:
        memory = {}

    matches = []

    keyword_lower = keyword.lower()

    for entry in memory.values():
        combined_text = " ".join([
            entry.get("file_path", ""),
            entry.get("description", ""),
            " ".join(entry.get("tags", []))
        ]).lower()

        if keyword_lower in combined_text:
            matches.append(entry)

    return {
        "matches": matches
    }

# ---- Metrics ----

@app.get("/metrics/summary")
def get_metrics_summary():
    """
    Return project-level delivery and reasoning metrics summary.
    """
    summary = generate_metrics_summary()
    reasoning_summary = generate_project_reasoning_summary()
    summary["reasoning_summary"] = reasoning_summary
    return summary

# ---- OpenAPI JSON Schema ----

@app.get("/openapi.json")
def serve_openapi():
    with open("openapi.json", "r") as f:
        return JSONResponse(content=json.load(f))

from fastapi.openapi.utils import get_openapi

def custom_openapi():
    with open("openapi.json", "r") as f:
        return json.load(f)

app.openapi = custom_openapi

@app.get("/actions/list")
def list_available_actions():
    with open("openapi.json", "r") as f:
        schema = json.load(f)

    grouped_actions = {}

    for path, methods in schema.get("paths", {}).items():
        for method, details in methods.items():
            # Skip non-standard methods just in case
            if method.lower() not in ["get", "post", "put", "patch", "delete"]:
                continue

            # Use tags if available, otherwise "General"
            tags = details.get("tags", ["General"])

            for tag in tags:
                if tag not in grouped_actions:
                    grouped_actions[tag] = []

                # Prefer x-gpt-action name, otherwise fall back to summary
                action_name = details.get("x-gpt-action", {}).get("name", details.get("summary", f"{method.upper()} {path}"))
                grouped_actions[tag].append(action_name)

    # Now format for response
    actions_response = []
    for tag, actions in grouped_actions.items():
        actions_response.append({
            "category": tag,
            "actions": actions
        })

    return {"actions": actions_response}