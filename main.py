# 📁 github_proxy/main.py

# ---- (1) Imports ----
from fastapi import FastAPI, HTTPException, Request, Body, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.openapi.utils import get_openapi
from fastapi import BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Optional, Union
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
import base64
import os
import time
from github import Github, GithubException
from openai import OpenAI
from dotenv import load_dotenv

# ---- (2) Global Variables ----
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"
GITHUB_REPO = "ai-delivery-framework"
GITHUB_OWNER = "stewmckendry"
TASK_FILE_PATH = "task.yaml"
GITHUB_BRANCH = "main"
PROMPT_DIR = "prompts/used"
MEMORY_FILE_PATH = "memory.yaml"
REASONING_FOLDER_PATH = ".logs/reasoning/"

g = Github(GITHUB_TOKEN)
repo = g.get_repo(GITHUB_OWNER + "/" + GITHUB_REPO)

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

"""  # <<< OLD
class PromotePatchRequest(BaseModel):
    task_id: str
    summary: str
    output_files: Dict[str, str]  # filename -> content mapping
    reasoning_trace: str
    prompt_path: Optional[str] = None
    output_folder: Optional[str] = None
    handoff_notes: Optional[str] = None  # <<< NEW
"""

class PromotePatchRequest(BaseModel):
    task_id: str
    summary: str
    output_files: dict  # { path: content }
    prompt_path: str
    reasoning_trace: str
    output_folder: str = "misc"
    handoff_notes: str = None


class MemoryFileEntry(BaseModel):
    file_path: str
    description: str
    tags: List[str]

class AddToMemoryRequest(BaseModel):
    files: List[MemoryFileEntry]

# ---- (4) Helper Functions ----
def fetch_task_yaml_from_github():
    try:
        file = repo.get_contents("task.yaml", ref=GITHUB_BRANCH)
        decoded = base64.b64decode(file.content).decode("utf-8")
        return yaml.safe_load(decoded)
    except GithubException as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch task.yaml: {str(e)}")

def fetch_yaml_from_github(file_path: str):
    try:
        file = repo.get_contents(file_path, ref=GITHUB_BRANCH)
        decoded = base64.b64decode(file.content).decode("utf-8")
        return yaml.safe_load(decoded)
    except GithubException as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch {file_path}: {str(e)}")

def fetch_file_content_from_github(file_path: str):
    try:
        file = repo.get_contents(file_path, ref=GITHUB_BRANCH)
        return base64.b64decode(file.content).decode("utf-8")
    except GithubException as e:
        raise HTTPException(status_code=404, detail=f"Failed to fetch {file_path}: {str(e)}")

def list_files_from_github(path):
    try:
        contents = repo.get_contents(path, ref=GITHUB_BRANCH)
        return [file.path for file in contents]
    except GithubException as e:
        raise HTTPException(status_code=404, detail=f"Failed to list files at {path}: {str(e)}")

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

# --- Utility Functions for Project Initialization ---

def run_project_initialization(project_name: str, repo_name: str, project_description: str):
    try:
        github_client = Github(GITHUB_TOKEN)

        framework_repo = github_client.get_repo("stewmckendry/ai-delivery-framework")
        project_repo = github_client.get_repo(f"stewmckendry/{repo_name}")

        framework_path = "framework"
        framework_dest_path = ""  # ⬅️ will stay clean
        project_base_path = "project"

        # Validate framework exists
        framework_repo.get_contents(framework_path)

        # Copy framework files
        copy_framework_baseline(framework_repo, project_repo, framework_path, framework_dest_path)

        # Create initial project files
        create_initial_files(project_repo, project_base_path, project_name, project_description)

        print(f"✅ Finished initializing project {project_name} into {repo_name}")

    except Exception as e:
        print(f"❌ Exception inside run_project_initialization: {type(e).__name__}: {e}")


def copy_framework_baseline(source_repo, destination_repo, source_path, dest_path):
    contents = source_repo.get_contents(source_path)
    for item in contents:
        if item.type == "dir":
            # Recursively copy subfolders
            new_dest_path = f"{dest_path}/{item.name}" if dest_path else item.name
            copy_framework_baseline(source_repo, destination_repo, item.path, new_dest_path)
        else:
            file_content_bytes = source_repo.get_contents(item.path).decoded_content
            try:
                file_content = file_content_bytes.decode('utf-8')
                destination_path = f"framework/{dest_path}/{item.name}" if dest_path else f"framework/{item.name}"
                destination_repo.create_file(destination_path, f"Copied {item.name} from framework", file_content)
            except UnicodeDecodeError:
                print(f"⚠️ Skipping binary file during copy: {item.path}")


def create_initial_files(project_repo, project_base_path, project_name, project_description):
    starter_task_yaml = f"""tasks:
  1.1_capture_project_goals:
    description: Help capture and summarize the goals, purpose, and intended impact of the project.
    phase: Phase 1 - Discovery
    category: discovery
    pod_owner: DeliveryPod
    status: pending
    prompt: prompts/used/{project_name}_capture_project_goals_prompt.txt
    inputs: []
    outputs:
      - outputs/project_goals.md
    ready: true
    done: false
    created_by: human
    created_at: {datetime.utcnow().isoformat()}
    updated_at: {datetime.utcnow().isoformat()}
"""

    starter_memory_yaml = f"""memory:
  context:
    project_name: {project_name}
    project_description: {project_description}
    created_at: {datetime.utcnow().isoformat()}
"""

    # Create under the project base path
    project_repo.create_file(f"{project_base_path}/task.yaml", "Initialize task.yaml", starter_task_yaml)
    project_repo.create_file(f"{project_base_path}/memory.yaml", "Initialize memory.yaml", starter_memory_yaml)

    # Outputs folder
    project_repo.create_file(f"{project_base_path}/outputs/project_init/prompt_used.txt", "Capture initial project prompt", f"Project: {project_name}\nDescription: {project_description}")
    project_repo.create_file(f"{project_base_path}/outputs/project_init/reasoning_trace.md", "Initial project reasoning trace", f"# Reasoning Trace for {project_name}\n\n- Project initialized with AI Native Delivery Framework.\n- Project Description: {project_description}\n- Initialization Date: {datetime.utcnow().isoformat()}")


def get_repo(repo_name: str):
    github_client = Github(GITHUB_TOKEN)
    return github_client.get_repo(f"stewmckendry/{repo_name}")


def commit_and_log(repo, file_path, content, commit_message):
    try:
        changelog_path = "project/outputs/changelog.yaml"
        try:
            changelog_file = repo.get_contents(changelog_path)
            changelog = yaml.safe_load(changelog_file.decoded_content) or []
            changelog_sha = changelog_file.sha
        except Exception:
            changelog = []
            changelog_sha = None

        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "files": [{"path": file_path, "change": commit_message}]
        }

        try:
            existing_file = repo.get_contents(file_path)
            repo.update_file(file_path, commit_message, content, existing_file.sha)
        except Exception:
            repo.create_file(file_path, commit_message, content)

        changelog.append(log_entry)
        changelog_content = yaml.dump(changelog)

        if changelog_sha:
            repo.update_file(changelog_path, f"Update changelog at {timestamp}", changelog_content, changelog_sha)
        else:
            repo.create_file(changelog_path, f"Create changelog at {timestamp}", changelog_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Commit and changelog failed: {str(e)}")



# ---- (5) API Routes ----

# ---- Root ----
@app.get("/")
async def root():
    return {"message": "GitHub File Proxy is running."}

# ---- GitHub File Proxy ----

@app.post("/getFile")
async def get_file(repo_name: str = Body(...), path: str = Body(...), ref: Optional[str] = Body(None)):
    try:
        repo = get_repo(repo_name)
        file = repo.get_contents(path, ref or GITHUB_BRANCH)
        content = file.decoded_content.decode()
        return {
            "path": file.path,
            "sha": file.sha,
            "content": content,
            "ref": ref or GITHUB_BRANCH
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/batch-files")
async def get_batch_files(repo_name: str = Body(...), paths: List[str] = Body(...), ref: Optional[str] = Body(GITHUB_BRANCH)):
    try:
        repo = get_repo(repo_name)
        results = []
        for path in paths:
            try:
                file = repo.get_contents(path, ref=ref)
                results.append({
                    "path": path,
                    "content": base64.b64decode(file.content).decode("utf-8")
                })
            except GithubException as e:
                results.append({
                    "path": path,
                    "error": str(e)
                })
        return {"files": results}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

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
async def activate_task(task_id: Union[str, List[str]] = Body(...), repo_name: str = Body(...)):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        if isinstance(task_id, str):
            task_ids = [task_id]
        else:
            task_ids = task_id

        planned_tasks = {}
        for t_id in task_ids:
            if t_id not in task_data.get("tasks", {}):
                raise HTTPException(status_code=400, detail=f"Task {t_id} not found in task.yaml.")
            task_data["tasks"][t_id]["status"] = "planned"
            planned_tasks[t_id] = task_data["tasks"][t_id]

        commit_and_log(repo, task_path, yaml.dump(task_data), f"Planned tasks {task_ids}")

        response = {
            "message": f"Tasks {task_ids} successfully planned.",
            "planned_tasks": [
                {
                    "task_id": t_id,
                    "pod_owner": planned_tasks[t_id].get("pod_owner"),
                    "metadata": planned_tasks[t_id]
                } for t_id in task_ids
            ]
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to activate task(s): {str(e)}")

@app.post("/tasks/start")
async def start_task(task_id: str = Body(...), repo_name: str = Body(...)):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        if task_id not in task_data.get("tasks", {}):
            raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found.")

        task = task_data["tasks"][task_id]
        task["status"] = "in_progress"
        task["updated_at"] = datetime.utcnow().isoformat()
        updated_task_yaml = yaml.dump(task_data, sort_keys=False)
        commit_and_log(repo, task_path, updated_task_yaml, f"Start task {task_id}")

        # Optional: fetch handoff
        handoff_note = None
        handoff_from = task.get("handoff_from")
        if handoff_from:
            try:
                handoff_file = repo.get_contents(f"project/outputs/{handoff_from}/handoff_notes.yaml")
                data = yaml.safe_load(handoff_file.decoded_content)
                handoff_note = data.get("handoffs", [])[-1] if data.get("handoffs") else None
            except Exception:
                handoff_note = None

        prompt_path = task.get("prompt")
        input_files = task.get("inputs", [])

        prompt_content = "Prompt file missing."
        if prompt_path:
            try:
                prompt_file = repo.get_contents(prompt_path)
                prompt_content = prompt_file.decoded_content.decode()
            except:
                prompt_content = "Prompt file missing."

        return {
            "message": f"Task {task_id} started successfully.",
            "prompt_content": prompt_content,
            "inputs": input_files,
            "handoff_note": handoff_note,
            "next_step": "Call /tasks/append_chain_of_thought to log 2–3 initial thoughts from GPT Pod."
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Internal Server Error: {type(e).__name__}: {e}"})

@app.post("/tasks/reopen")
async def reopen_task(repo_name: str = Body(...), task_id: str = Body(...), reason: Optional[str] = Body("Reopening for further work.")):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        if task_id not in task_data.get("tasks", {}):
            raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

        task_data["tasks"][task_id]["status"] = "in_progress"
        task_data["tasks"][task_id]["updated_at"] = datetime.utcnow().isoformat()
        updated_content = yaml.dump(task_data)
        commit_and_log(repo, task_path, updated_content, f"Reopen task {task_id}")

        # Append to chain of thought
        cot_path = f"project/outputs/{task_id}/chain_of_thought.yaml"
        cot_message = {
            "timestamp": datetime.utcnow().isoformat(),
            "message": reason
        }
        try:
            cot_file = repo.get_contents(cot_path)
            cot_data = yaml.safe_load(cot_file.decoded_content) or []
            cot_data.append(cot_message)
            commit_and_log(repo, cot_path, yaml.dump(cot_data), f"Append COT reopen note for {task_id}")
        except:
            commit_and_log(repo, cot_path, yaml.dump([cot_message]), f"Initialize COT for {task_id}")

        return {"message": f"Task {task_id} reopened and note added to chain of thought."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
@app.post("/tasks/next")
async def get_next_task(repo_name: str = Body(...), pod_owner: str = Body(...)):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        next_tasks = [
            {"task_id": tid, **tdata}
            for tid, tdata in task_data.get("tasks", {}).items()
            if tdata.get("status") in ["planned", "backlog"] and tdata.get("pod_owner") == pod_owner
        ]

        if not next_tasks:
            return {"message": f"No planned or backlog tasks for {pod_owner}."}

        next_tasks = sorted(next_tasks, key=lambda x: x.get("updated_at", x.get("created_at", "")))
        return {"next_task": next_tasks[0]}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

    
@app.post("/tasks/clone")
async def clone_task(
    repo_name: str = Body(...),
    original_task_id: str = Body(...),
    descriptor: str = Body(...)):

    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_yaml_file = repo.get_contents(task_path)
        tasks = yaml.safe_load(task_yaml_file.decoded_content)

        if original_task_id not in tasks["tasks"]:
            raise HTTPException(status_code=404, detail="Original task not found")

        original = tasks["tasks"][original_task_id].copy()
        new_task_id = f"{original_task_id}_clone_{descriptor}"
        original["status"] = "backlog"
        original["created_at"] = datetime.utcnow().isoformat()
        original["updated_at"] = original["created_at"]
        tasks["tasks"][new_task_id] = original

        updated_yaml = yaml.dump(tasks)
        commit_and_log(repo, task_path, updated_yaml, f"Clone task {original_task_id} as {new_task_id}")

        return {"message": "Task cloned", "new_task_id": new_task_id, "cloned_task_metadata": original}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clone task: {str(e)}")


@app.post("/tasks/append_chain_of_thought")
async def append_chain_of_thought(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    message: str = Body(...)):

    try:
        repo = get_repo(repo_name)
        cot_path = f"project/outputs/{task_id}/chain_of_thought.yaml"

        try:
            cot_file = repo.get_contents(cot_path)
            chain = yaml.safe_load(cot_file.decoded_content) or []
        except Exception:
            chain = []

        new_thought = {"timestamp": datetime.utcnow().isoformat(), "message": message}
        chain.append(new_thought)
        content = yaml.dump(chain)

        commit_and_log(repo, cot_path, content, f"Append chain of thought for {task_id}")

        return {"message": "Chain of thought updated", "appended_thought": new_thought}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to append chain of thought: {str(e)}")


@app.post("/tasks/append_handoff_note/{task_id}")
async def append_handoff_note(
    task_id: str,
    repo_name: str = Body(...),
    from_pod: str = Body(...),
    to_pod: str = Body(...),
    reason: str = Body(...),
    token_count: int = Body(...),
    next_prompt: str = Body(...),
    reference_files: list[str] = Body(default=[]),
    notes: str = Body(default=""),
    ways_of_working: str = Body(default="")
):
    repo = get_repo(repo_name)
    file_path = f"project/outputs/{task_id}/handoff_notes.yaml"

    try:
        file = repo.get_contents(file_path)
        handoff_data = yaml.safe_load(file.decoded_content) or {}
    except Exception:
        handoff_data = {}

    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "from_pod": from_pod,
        "to_pod": to_pod,
        "reason": reason,
        "token_count": token_count,
        "next_prompt": next_prompt,
        "reference_files": reference_files,
        "notes": notes,
        "ways_of_working": ways_of_working
    }

    handoff_data.setdefault("handoffs", []).append(new_entry)
    updated_yaml = yaml.dump(handoff_data, sort_keys=False)

    commit_and_log(repo, file_path, updated_yaml, f"Append handoff note to task {task_id}")

    return {"message": "Handoff note appended", "note": new_entry}

@app.post("/tasks/fetch_handoff_note")
async def fetch_handoff_note(
    repo_name: str = Body(...),
    task_id: str = Body(...)
):
    repo = get_repo(repo_name)
    task_path = "project/task.yaml"
    try:
        task_file = repo.get_contents(task_path)
        tasks = yaml.safe_load(task_file.decoded_content)
        task = tasks.get("tasks", {}).get(task_id, {})
        handoff_from = task.get("handoff_from")
        if not handoff_from:
            return {"message": "No handoff_from reference in task metadata."}

        handoff_path = f"project/outputs/{handoff_from}/handoff_notes.yaml"
        file = repo.get_contents(handoff_path)
        notes_data = yaml.safe_load(file.decoded_content)
        latest_note = notes_data.get("handoffs", [])[-1] if notes_data.get("handoffs") else None
        return {"handoff_from": handoff_from, "handoff_note": latest_note}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


# LEGACY TOOL - TO BE DEPRECATED / REMOVED
@app.post("/tasks/auto_commit")
async def auto_commit(
    repo_name: str = Body(...),
    commit_message: str = Body(...),
    updates: List[Dict[str, str]] = Body(...)
):
    try:
        github_client = Github(GITHUB_TOKEN)
        repo = github_client.get_repo(f"stewmckendry/{repo_name}")

        for update in updates:
            file_path = update["file"]
            content = update["content"]
            try:
                existing_file = repo.get_contents(file_path)
                repo.update_file(
                    path=file_path,
                    message=commit_message,
                    content=content,
                    sha=existing_file.sha
                )
            except Exception:
                repo.create_file(
                    path=file_path,
                    message=commit_message,
                    content=content
                )

        # Update the auto-commit marker
        marker_path = ".logs/last_autocommit_marker.txt"
        try:
            marker_file = repo.get_contents(marker_path)
            new_marker_content = f"Last auto-commit at {datetime.utcnow().isoformat()}"
            repo.update_file(marker_path, "Update auto-commit marker", new_marker_content, sha=marker_file.sha)
        except Exception:
            new_marker_content = f"First auto-commit at {datetime.utcnow().isoformat()}"
            repo.create_file(marker_path, "Create auto-commit marker", new_marker_content)

        return {"message": f"Auto-commit done for {repo_name} with message: {commit_message}"}

    except Exception as e:
        print(f"❌ Exception during auto_commit: {type(e).__name__}: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Internal Server Error: {type(e).__name__}: {e}"})

@app.post("/tasks/update_changelog/{task_id}")
async def update_changelog(
    task_id: str,
    repo_name: str = Body(...),
    changelog_message: str = Body(...)
):
    try:
        github_client = Github(GITHUB_TOKEN)
        repo = github_client.get_repo(f"stewmckendry/{repo_name}")

        changelog_path = "project/outputs/CHANGELOG.md"

        try:
            existing_changelog = repo.get_contents(changelog_path)
            old_content = existing_changelog.decoded_content.decode()
            new_entry = f"\n## Task {task_id}\n- {changelog_message}\n- Timestamp: {datetime.utcnow().isoformat()}\n"
            new_content = old_content + new_entry
            repo.update_file(
                changelog_path,
                f"Update CHANGELOG for task {task_id}",
                new_content,
                sha=existing_changelog.sha
            )
        except Exception:
            # Create new if doesn't exist
            new_content = f"# Project Changelog\n\n## Task {task_id}\n- {changelog_message}\n- Timestamp: {datetime.utcnow().isoformat()}\n"
            repo.create_file(
                changelog_path,
                f"Create initial CHANGELOG with task {task_id}",
                new_content
            )

        return {"message": f"Changelog updated for task {task_id}."}

    except Exception as e:
        print(f"\u274c Exception during update_changelog: {type(e).__name__}: {e}")
        return JSONResponse(status_code=500, content={"detail": f"Internal Server Error: {type(e).__name__}: {e}"})


@app.post("/tasks/complete")
async def complete_task(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    outputs: Optional[List[dict]] = Body(None),
    reasoning_trace: Optional[dict] = Body(None),
    handoff_note: Optional[dict] = Body(default={})):

    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        if task_id not in task_data.get("tasks", {}):
            raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found.")

        task_data["tasks"][task_id]["status"] = "completed"
        task_data["tasks"][task_id]["done"] = True
        task_data["tasks"][task_id]["updated_at"] = datetime.utcnow().isoformat()
        commit_and_log(repo, task_path, yaml.dump(task_data), f"Mark task {task_id} as completed")

        output_dir = f"project/outputs/{task_id}"
        for item in outputs:
            output_path = item["path"]
            output_content = item["content"]
            commit_and_log(repo, output_path, output_content, f"Save output for {task_id}")

        if reasoning_trace:
            trace_path = f"{output_dir}/reasoning_trace.yaml"
            commit_and_log(repo, trace_path, yaml.dump(reasoning_trace), f"Log reasoning trace for {task_id}")

        if handoff_note:
            handoff_path = f"{output_dir}/handoff_notes.yaml"
            try:
                file = repo.get_contents(handoff_path)
                handoff_data = yaml.safe_load(file.decoded_content) or {}
            except:
                handoff_data = {}

            handoff_data.setdefault("handoffs", []).append(handoff_note)
            commit_and_log(repo, handoff_path, yaml.dump(handoff_data, sort_keys=False), f"Log handoff note for {task_id}")

        return {"message": f"Task {task_id} completed and outputs committed."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})


# LEGACY TOOL - TO BE DEPRECATED / REMOVED
@app.post("/patches/promote")
async def promote_patch(
    request: PromotePatchRequest,
):
    task_id = request.task_id
    summary = request.summary
    output_files = request.output_files
    reasoning_trace = request.reasoning_trace
    prompt_path = request.prompt_path
    output_folder = request.output_folder
    handoff_notes = request.handoff_notes
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

    # Fetch task.yaml to get category and pod_owner
    task_path = "project/task.yaml"
    task_file = repo.get_contents(task_path, ref=GITHUB_BRANCH)
    task_data = yaml.safe_load(base64.b64decode(task_file.content))

    task_meta = task_data.get("tasks", {}).get(task_id)
    if not task_meta:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found in task.yaml")

    category = task_meta.get("category", "misc")
    pod_owner = task_meta.get("pod_owner", "misc")

    branch_name = f"chatgpt/auto/{category}/{task_id}"

    # Create new branch
    main_ref = repo.get_branch(GITHUB_BRANCH)
    try:
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=main_ref.commit.sha)
    except GithubException as e:
        if e.status != 422:
            raise e

    def create_or_update_file(file_path: str, content: str, commit_message: str):
        try:
            existing_file = repo.get_contents(file_path, ref=branch_name)
            repo.update_file(file_path, commit_message, content, existing_file.sha, branch=branch_name)
        except GithubException as e:
            if e.status == 404:
                repo.create_file(file_path, commit_message, content, branch=branch_name)
            else:
                raise

    # Upload output files
    for file_path, file_content in output_files.items():
        create_or_update_file(
            file_path,
            file_content,
            commit_message=f"[Auto] Add or update {file_path} for task {task_id}"
        )

    # Upload reasoning trace
    reasoning_path = f".logs/reasoning/{task_id}_{timestamp}_reasoning_trace.md"
    create_or_update_file(
        reasoning_path,
        reasoning_trace,
        commit_message=f"[Auto] Add or update reasoning trace for task {task_id}"
    )

    # Upload changelog
    changelog_content = f"""# Changelog for Task {task_id}

    ## Summary
    {summary}

    ## Files Added or Updated
    {chr(10).join([f"- {path}" for path in output_files.keys()])}

    ## Reasoning Trace
    See `.logs/reasoning/{task_id}_{timestamp}_reasoning_trace.md`

    ## Prompt Used
    See `.logs/prompts/{pod_owner}/{task_id}_{timestamp}_prompt.txt`
    """

    changelog_path = f".logs/changelogs/{task_id}_{timestamp}_changelog.md"
    create_or_update_file(
        changelog_path,
        changelog_content,
        commit_message=f"[Auto] Add changelog for task {task_id}"
    )

    # Upload handoff notes
    if handoff_notes:
        handoff_path = f".logs/handoff/{task_id}_{timestamp}_handoff.md"
        create_or_update_file(
            handoff_path,
            handoff_notes,
            commit_message=f"[Auto] Add or update handoff notes for task {task_id}"
        )

    # Upload prompt used
    if prompt_path:
        prompt_log_path = f".logs/prompts/{pod_owner}/{task_id}_{timestamp}_prompt.txt"
        create_or_update_file(
            prompt_log_path,
            f"Prompt used for task {task_id}: {prompt_path}",
            commit_message=f"[Auto] Save prompt used for task {task_id}"
        )

    # Update memory.yaml
    memory_path = "project/memory.yaml"
    memory_file = repo.get_contents(memory_path, ref=branch_name)
    memory_data = yaml.safe_load(base64.b64decode(memory_file.content))

    def smart_merge_memory(memory, key, file_path, description, tags):
        existing_entry = memory.get(key)
        if existing_entry:
            if existing_entry.get("description", "").startswith("Output file generated from task") or not existing_entry.get("description"):
                existing_entry["description"] = description
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

    # Update memory entries
    for file_path in output_files.keys():
        key = file_path.replace("/", "_").replace(".", "_")
        smart_merge_memory(memory_data, key, file_path, f"Output file generated from task {task_id}", ["project", "outputs"])

    trace_key = f"logs_reasoning_{task_id}_reasoning_trace_md"
    smart_merge_memory(memory_data, trace_key, reasoning_path, f"Reasoning trace for task {task_id}", ["project", "reasoning"])

    if prompt_path:
        prompt_key = prompt_path.replace("/", "_").replace(".", "_")
        smart_merge_memory(memory_data, prompt_key, prompt_log_path, f"Prompt used for task {task_id}", ["project", "prompt"])

    new_memory_yaml = yaml.safe_dump(memory_data, sort_keys=False)
    repo.update_file(
        path=memory_path,
        message=f"[Auto] Update memory.yaml for task {task_id}",
        content=new_memory_yaml,
        sha=memory_file.sha,
        branch=branch_name
    )

    # Create PR
    paths_list = ''.join([f"- New or updated file: `{path}`\n" for path in output_files.keys()])

    pr_body = f"""
    ## ✨ What was added?
    - Covers task: `{task_id}`
    {paths_list}

    ## 🎯 Why it matters
    {summary}

    ## 🧠 Thought process
    See `.logs/reasoning/{task_id}_{timestamp}_reasoning_trace.md`

    ## 📄 Related
    - Task ID: {task_id}
    - Changelog: `.logs/changelogs/{task_id}_{timestamp}_changelog.md`
    - Prompt snapshot saved: `.logs/prompts/{pod_owner}/{task_id}_{timestamp}_prompt.txt`
    """

    pr = repo.create_pull(
        title=f"Promote patch for {task_id}",
        body=pr_body,
        head=branch_name,
        base=GITHUB_BRANCH
    )

    return {
        "pr_url": pr.html_url,
        "branch_name": branch_name
    }


"""
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
"""


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
async def update_task_metadata(task_id: str, 
                                description: Optional[str] = None,
                                prompt: Optional[str] = None,
                                inputs: Optional[list] = None,
                                outputs: Optional[list] = None,
                                ready: Optional[bool] = None,
                                done: Optional[bool] = None):
    # Load task.yaml
    with open("task.yaml", "r") as f:
        tasks = yaml.safe_load(f)

    if task_id not in tasks["tasks"]:
        raise HTTPException(status_code=404, detail="Task not found")

    task = tasks["tasks"][task_id]
    # Update fields
    if description: task["description"] = description
    if prompt: task["prompt"] = prompt
    if inputs: task["inputs"] = inputs
    if outputs: task["outputs"] = outputs
    if ready is not None: task["ready"] = ready
    if done is not None: task["done"] = done
    task["updated_at"] = datetime.utcnow().isoformat()

    # Save task.yaml
    with open("task.yaml", "w") as f:
        yaml.dump(tasks, f)

    # Auto-commit update
    await auto_commit({
        "repo_name": "nhl-predictor",
        "commit_message": f"Update task metadata: {task_id}",
        "updates": [{"file": "task.yaml", "content": yaml.dump(tasks)}]
    })

    return {"message": "Task metadata updated", "task_id": task_id, "updated_task_metadata": task}

@app.patch("/tasks/update_metadata")
async def update_task_metadata(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    description: Optional[str] = None,
    prompt: Optional[str] = None,
    inputs: Optional[list] = None,
    outputs: Optional[list] = None,
    ready: Optional[bool] = None,
    done: Optional[bool] = None):

    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_yaml_file = repo.get_contents(task_path)
        tasks = yaml.safe_load(task_yaml_file.decoded_content)

        if task_id not in tasks["tasks"]:
            raise HTTPException(status_code=404, detail="Task not found")

        task = tasks["tasks"][task_id]
        if description: task["description"] = description
        if prompt: task["prompt"] = prompt
        if inputs: task["inputs"] = inputs
        if outputs: task["outputs"] = outputs
        if ready is not None: task["ready"] = ready
        if done is not None: task["done"] = done
        task["updated_at"] = datetime.utcnow().isoformat()

        updated_yaml = yaml.dump(tasks)
        commit_and_log(repo, task_path, updated_yaml, f"Update metadata for {task_id}")

        return {"message": "Task metadata updated", "task_id": task_id, "updated_task_metadata": task}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update metadata: {str(e)}")


# ---- Memory Management ----

@app.post("/memory/index")
async def index_memory(repo_name: str = Body(...), base_paths: Optional[List[str]] = None):
    try:
        repo = get_repo(repo_name)
        memory_path = "project/memory.yaml"
        memory = []
        base_paths = base_paths or []

        def recurse_files(path):
            entries = repo.get_contents(path)
            if not isinstance(entries, list):
                entries = [entries]
            for entry in entries:
                if entry.type == "file":
                    memory.append({
                        "path": entry.path,
                        "raw_url": entry.download_url,
                        "file_type": entry.name.split(".")[-1] if "." in entry.name else "unknown",
                        "description": "",
                        "tags": [],
                        "last_updated": datetime.utcnow().date().isoformat(),
                        "pod_owner": ""
                    })
                elif entry.type == "dir":
                    recurse_files(entry.path)

        for base_path in base_paths:
            try:
                recurse_files(base_path)
            except Exception:
                continue

        memory_content = yaml.dump(memory)
        commit_and_log(repo, memory_path, memory_content, f"Indexed {len(memory)} memory entries")

        return {"message": f"Memory indexed with {len(memory)} entries."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
        
@app.post("/memory/diff")
def memory_diff(repo_name: str = Body(...), base_paths: List[str] = Body(default=[])):
    try:
        repo = get_repo(repo_name)
        try:
            memory_path = "project/memory.yaml"
            memory_file = repo.get_contents(memory_path)
            memory = yaml.safe_load(memory_file.decoded_content) or []
        except Exception:
            memory = []

        memory_paths = {entry["path"] for entry in memory if "path" in entry}
        missing_files = []

        for path in base_paths:
            try:
                contents = repo.get_contents(path)
                if not isinstance(contents, list):
                    contents = [contents]
                for item in contents:
                    if item.path not in memory_paths:
                        missing_files.append(item.path)
            except:
                continue

        return {"message": f"Found {len(missing_files)} missing files", "missing_files": missing_files}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/memory/add")
async def add_to_memory(repo_name: str = Body(...), files: List[dict] = Body(...)):
    try:
        repo = get_repo(repo_name)
        memory_path = "project/memory.yaml"
        try:
            memory_file = repo.get_contents(memory_path)
            memory = yaml.safe_load(memory_file.decoded_content) or []
        except Exception:
            memory = []

        memory.extend(files)
        memory_content = yaml.dump(memory)
        repo.update_file(memory_path, f"Add {len(files)} entries to memory", memory_content, memory_file.sha)

        return {"message": "New memory entries added", "memory_index": files}
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/memory/validate-files")
def validate_memory_file_exists(repo_name: str = Body(...), files: List[str] = Body(...)):
    try:
        repo = get_repo(repo_name)
        try:
            memory_path = "project/memory.yaml"
            memory_file = repo.get_contents(memory_path)
            memory = yaml.safe_load(memory_file.decoded_content) or []
        except Exception:
            memory = []

        memory_paths = {entry.get("path") for entry in memory if "path" in entry}
        results = []

        for file_path in files:
            memory_match = file_path in memory_paths
            github_match = False
            try:
                repo.get_contents(file_path)
                github_match = True
            except:
                github_match = False

            results.append({
                "file_path": file_path,
                "exists_in_memory": memory_match,
                "exists_in_github": github_match
            })

        return {"validated_files": results}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

@app.post("/memory/search")
def search_memory(repo_name: str = Body(...), keyword: str = Body(...)):
    try:
        repo = get_repo(repo_name)
        try:
            memory_path = "project/memory.yaml"
            memory_file = repo.get_contents(memory_path)
            memory = yaml.safe_load(memory_file.decoded_content) or []
        except Exception:
            memory = []

        keyword_lower = keyword.lower()
        matches = []

        for entry in memory:
            text = " ".join([
                entry.get("path", ""),
                entry.get("description", ""),
                " ".join(entry.get("tags", []))
            ]).lower()
            if keyword_lower in text:
                matches.append(entry)

        return {"matches": matches}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
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

# ---- Project Initialization ----

from fastapi import BackgroundTasks

@app.post("/project/init_project")
async def init_project(
    background_tasks: BackgroundTasks,
    project_name: str = Body(...),
    repo_name: str = Body(...),
    project_description: str = Body(...)
):
    try:
        print(f"🚀 Project init requested for {project_name} into repo {repo_name}")

        background_tasks.add_task(run_project_initialization, project_name, repo_name, project_description)

        return {"message": "Project initialization started. Check GitHub repo in 1-2 minutes."}

    except Exception as e:
        print(f"❌ Exception during init_project: {type(e).__name__}: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal Server Error: {type(e).__name__}: {e}"}
        )


# ---- OpenAPI JSON Schema ----

# --- Load openapi.json once at startup ---
try:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, "openapi.json")
    print(f"Current working directory: {os.getcwd()}")
    print(f"Files in {dir_path}: {os.listdir(dir_path)}")
    with open(file_path, "r") as f:
        openapi_schema = json.load(f)
    # Minimal validation: check if it has required fields
    if "openapi" not in openapi_schema or "paths" not in openapi_schema:
        raise ValueError("Invalid OpenAPI schema: missing 'openapi' or 'paths'")
    app.openapi_schema = openapi_schema
    print("✅ Successfully loaded openapi.json at startup.")
except Exception as e:
    print(f"❌ Failed to load openapi.json: {e}")
    openapi_schema = None
    app.openapi_schema = None

# --- Override app.openapi ---
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    raise RuntimeError("OpenAPI schema is not loaded properly.")

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