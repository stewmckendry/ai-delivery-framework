# 📁 github_proxy/main.py

# ---- (1) Imports ----
from fastapi import FastAPI, HTTPException, Request, Body, Query, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, PlainTextResponse
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
from utils.github_retry import with_retries

# ---- (2) Global Variables ----
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"
GITHUB_REPO = "ai-delivery-framework"
GITHUB_OWNER = "stewmckendry"
GITHUB_BRANCH = "main"
PROMPT_DIR = "prompts/used"
MEMORY_FILE_PATH = "project/memory.yaml"
TASK_FILE_PATH = "project/task.yaml"
REASONING_FOLDER_PATH = "project/outputs/"

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

def fetch_yaml_from_github(repo_name: str, path: str):
    try:
        repo = get_repo(repo_name)
        file = repo.get_contents(path)
        return yaml.safe_load(file.decoded_content)
    except Exception as e:
        print(f"Error fetching YAML from {path}: {e}")
        return {}

def fetch_file_content_from_github(repo_name: str, path: str):
    try:
        repo = get_repo(repo_name)
        return repo.get_contents(path).decoded_content.decode("utf-8")
    except Exception as e:
        print(f"Error fetching file content from {path}: {e}")
        return ""
    
def list_files_from_github(repo_name: str, path: str):
    try:
        repo = get_repo(repo_name)
        contents = repo.get_contents(path)
        return [file.path for file in contents]
    except Exception as e:
        print(f"Error listing files from {path}: {e}")
        return []
    
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

def get_pod_owner(repo, task_id: str, fallback: str = "unknown") -> str:
    """Fetch pod_owner from task.yaml in the GitHub repo."""
    try:
        task_file = repo.get_contents("project/task.yaml")
        task_data = yaml.safe_load(task_file.decoded_content)
        return task_data.get("tasks", {}).get(task_id, {}).get("pod_owner", fallback)
    except Exception:
        return fallback

def describe_file_for_memory(path, content):
    try:
        prompt = f"""
You are helping index files in an AI-native delivery repository.
Given the following file content from `{path}`, generate:
1. A short description of what this file contains
2. A list of 2–4 relevant tags (e.g. 'prompt', 'flow', 'model', 'config')
3. The pod likely to own or use this file (choose between DevPod, QAPod, ResearchPod, DeliveryPod, or leave blank)

File content:
---
{content[:3000]}
---

Respond with a YAML object with fields: description, tags (list), and pod_owner.
"""
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        parsed = yaml.safe_load(response.choices[0].message.content)
        return {
            "description": parsed.get("description", f"Generated summary for {path}"),
            "tags": parsed.get("tags", ["auto"]),
            "pod_owner": parsed.get("pod_owner", "")
        }
    except Exception:
        return {
            "description": f"Fallback summary for {path}",
            "tags": ["auto"],
            "pod_owner": ""
        }

def generate_metrics_summary(repo_name: str = "nhl-predictor"):
    task_data = fetch_yaml_from_github(repo_name, TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})
    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks.values() if t.get("done", False))

    # Cycle time
    cycle_times = []
    for t in tasks.values():
        if t.get("done") and t.get("created_at") and t.get("updated_at"):
            created = datetime.fromisoformat(t["created_at"])
            updated = datetime.fromisoformat(t["updated_at"])
            cycle_times.append((updated - created).total_seconds() / (3600 * 24))

    avg_cycle_time = sum(cycle_times) / len(cycle_times) if cycle_times else None

    # Reasoning traces from YAML
    scores = []
    recalls = 0
    novelties = 0
    total_logs = 0

    trace_paths = list_files_from_github(repo_name, REASONING_FOLDER_PATH)
    for path in trace_paths:
        if path.endswith("reasoning_trace.yaml"):
            try:
                trace = fetch_yaml_from_github(repo_name, path)
                
                score = trace.get("scoring", {}).get("thought_quality")
                if score is not None:
                    scores.append(score)
                if trace.get("scoring", {}).get("recall_used"):
                    recalls += 1
                if trace.get("scoring", {}).get("novel_insight"):
                    novelties += 1
                total_logs += 1
            except Exception:
                continue

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "quantitative": {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate_percent": (completed_tasks / total_tasks * 100) if total_tasks else 0,
            "average_cycle_time_days": avg_cycle_time,
            "patch_success_rate_percent": None
        },
        "qualitative": {
            "average_thought_quality_score": (sum(scores) / len(scores)) if scores else None,
            "recall_usage_percent": (recalls / total_logs * 100) if total_logs else 0,
            "novelty_rate_percent": (novelties / total_logs * 100) if total_logs else 0
        }
    }

def generate_project_reasoning_summary(repo_name: str = "nhl-predictor"):
    trace_paths = list_files_from_github(repo_name, REASONING_FOLDER_PATH)
    all_thoughts = []  # Includes thoughts, alternatives, improvements

    for path in trace_paths:
        if path.endswith("reasoning_trace.yaml"):
            try:
                trace = fetch_yaml_from_github(repo_name, path)
                for t in trace.get("thoughts", []):
                    all_thoughts.append(t.get("thought", ""))
                all_thoughts.extend(trace.get("alternatives", []))
                all_thoughts.extend(trace.get("improvement_opportunities", []))
            except Exception:
                continue

    merged_thoughts = "\n".join(all_thoughts[:100])

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
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()


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


def commit_and_log(repo, file_path, content, commit_message, task_id: Optional[str] = None, committed_by: Optional[str] = None):
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
            "path": file_path,
            "task_id": task_id,
            "committed_by": committed_by,
            "message": commit_message
        }

        try:
            existing_file = repo.get_contents(file_path)
            repo.update_file(file_path, commit_message, content, existing_file.sha)
        except Exception:
            repo.create_file(file_path, commit_message, content)

        changelog.append(log_entry)
        changelog_content = yaml.dump(changelog, sort_keys=False)

        if changelog_sha:
            repo.update_file(changelog_path, f"Update changelog at {timestamp}", changelog_content, changelog_sha)
        else:
            repo.create_file(changelog_path, f"Create changelog at {timestamp}", changelog_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Commit and changelog failed: {str(e)}")
    
def generate_handoff_note(task_id: str, repo) -> dict:
        task_path = "project/task.yaml"
        cot_path = f"project/outputs/{task_id}/chain_of_thought.yaml"
        try:
            task_file = repo.get_contents(task_path)
            tasks = yaml.safe_load(task_file.decoded_content)
            task = tasks.get("tasks", {}).get(task_id, {})
            pod_owner = task.get("pod_owner", "Unknown")
            description = task.get("description", "")

            # Load all chain of thought messages
            try:
                cot_file = repo.get_contents(cot_path)
                cot_data = yaml.safe_load(cot_file.decoded_content)
                all_thoughts = [entry.get("message", "") for entry in cot_data.get("thoughts", []) if "message" in entry]
                notes = "\n".join(all_thoughts[-5:])  # capture last 5 thoughts
            except:
                notes = ""

            # Collect output file paths for reference
            output_paths = task.get("outputs", [])
            reference_files = output_paths + [f"project/outputs/{task_id}/"]

            return {
                "timestamp": datetime.utcnow().isoformat(),
                "from_pod": pod_owner,
                "to_pod": "<replace with who the next pod is, or ask the human to confirm>",  # GPT or Human must fill in
                "reason": "Auto-generated handoff on task completion.",
                "token_count": 0,
                "next_prompt": f"Follow up based on task: {description}",
                "reference_files": reference_files,
                "notes": notes,
                "ways_of_working": "Continue using async updates and reasoning logs."
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error generating handoff note: {str(e)}")
        
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

        pod_owner = get_pod_owner(repo, task_id)
        commit_and_log(repo, task_path, yaml.dump(task_data), f"Planned tasks {task_ids}", task_id=task_id, committed_by=pod_owner)

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

# PATCHED /tasks/start route: Adds prompt_used.txt logging (cleaned up)

@app.post("/tasks/start")
async def start_task(task_id: str = Body(...), repo_name: str = Body(...), prompt_used: Optional[str] = Body(default=None)):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        if task_id not in task_data.get("tasks", {}):
            from difflib import get_close_matches
            close = get_close_matches(task_id, task_data.get("tasks", {}).keys(), n=3, cutoff=0.4)
            raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found. Suggestions: {close}")

        task = task_data["tasks"][task_id]
        task["status"] = "in_progress"
        task["updated_at"] = datetime.utcnow().isoformat()

        # Save prompt_used.txt
        if prompt_used:
            prompt_path = f"project/outputs/{task_id}/prompt_used.txt"
            commit_and_log(repo, prompt_path, prompt_used, f"Log prompt used for task {task_id}", task_id=task_id, committed_by=task.get("pod_owner", "GPTPod"))
            task["prompt_used"] = prompt_path

        # Update task.yaml
        updated_task_yaml = yaml.dump(task_data, sort_keys=False)
        commit_and_log(repo, task_path, updated_task_yaml, f"Start task {task_id}", task_id=task_id, committed_by=task.get("pod_owner", "unknown"))

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

        # Get input files list
        input_files = task.get("inputs", [])

        # Get reasoning trace summary from previous task (optional)
        reasoning_summary = None
        try:
            rt_file = repo.get_contents(f"project/outputs/{handoff_from}/reasoning_trace.yaml")
            rt_data = yaml.safe_load(rt_file.decoded_content)
            reasoning_summary = rt_data.get("summary")
        except:
            reasoning_summary = None

        return {
            "message": f"Task {task_id} started successfully.",
            "inputs": input_files,
            "handoff_note": handoff_note,
            "reasoning_summary": reasoning_summary,
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
        commit_and_log(repo, task_path, updated_content, f"Reopen task {task_id}", task_id=task_id, committed_by=task_data["tasks"][task_id]["pod_owner"])

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
            commit_and_log(repo, cot_path, yaml.dump(cot_data), f"Append COT reopen note for {task_id}", task_id=task_id, committed_by=task_data["tasks"][task_id]["pod_owner"])
        except:
            commit_and_log(repo, cot_path, yaml.dump([cot_message]), f"Initialize COT for {task_id}", task_id=task_id, committed_by=task_data["tasks"][task_id]["pod_owner"])

        return {"message": f"Task {task_id} reopened and note added to chain of thought."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})
    
@app.post("/tasks/next")
def get_next_task(
    repo_name: str = Body(...),
    pod_owner: Optional[str] = Body(default=None)
):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_file = repo.get_contents(task_path)
        task_data = yaml.safe_load(task_file.decoded_content)

        # Filter tasks marked as planned or backlog and matching pod_owner (if provided)
        candidates = [
            {"task_id": tid, "description": t.get("description", ""), "status": t.get("status")}
            for tid, t in task_data.get("tasks", {}).items()
            if t.get("status") in ["planned", "backlog"] and (not pod_owner or t.get("pod_owner") == pod_owner)
        ]

        if not candidates:
            return {"message": "No ready tasks found for this Pod."}

        return {
            "message": f"Found {len(candidates)} task(s) for pod {pod_owner or 'any'}.",
            "tasks": candidates,
            "next_step": "Choose a task_id and call /tasks/start to begin."
        }
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
        pod_owner = get_pod_owner(repo, original_task_id)
        commit_and_log(repo, task_path, updated_yaml, f"Clone task {original_task_id} as {new_task_id}", task_id=new_task_id, committed_by=pod_owner)

        return {"message": "Task cloned", "new_task_id": new_task_id, "cloned_task_metadata": original}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clone task: {str(e)}")

@app.post("/tasks/commit_and_log_output")
async def commit_and_log_output(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    file_path: str = Body(...),
    content: str = Body(...),
    message: str = Body(...),
    committed_by: Optional[str] = Body("GPTPod")
):
    try:
        repo = get_repo(repo_name)

        # Update file and changelog
        commit_and_log(
            repo,
            file_path=file_path,
            content=content,
            commit_message=message,
            task_id=task_id,
            committed_by=committed_by
        )

        # Append path to task.yaml[outputs]
        task_file = repo.get_contents("project/task.yaml")
        task_data = yaml.safe_load(task_file.decoded_content)
        task = task_data["tasks"].get(task_id, {})
        outputs = task.get("outputs", [])
        if file_path not in outputs:
            outputs.append(file_path)
            task["outputs"] = outputs
            updated_yaml = yaml.dump(task_data, sort_keys=False)
            commit_and_log(
                repo,
                file_path="project/task.yaml",
                content=updated_yaml,
                commit_message=f"Append output file to {task_id}",
                task_id=task_id,
                committed_by=committed_by
            )

        return {"message": f"Output file {file_path} committed and logged for task {task_id}."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Commit failed: {str(e)}"})


@app.post("/tasks/append_chain_of_thought")
async def append_chain_of_thought(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    message: str = Body(...),
    tags: Optional[List[str]] = Body(default=None),
    issues: Optional[List[str]] = Body(default=None),
    lessons: Optional[List[str]] = Body(default=None),
):
    try:
        repo = get_repo(repo_name)
        path = f"project/outputs/{task_id}/chain_of_thought.yaml"

        try:
            file = repo.get_contents(path)
            data = yaml.safe_load(file.decoded_content) or []
            sha = file.sha
        except:
            data = []
            sha = None

        entry = {
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        if tags:
            entry["tags"] = tags
        if issues:
            entry["issues"] = issues
        if lessons:
            entry["lessons"] = lessons

        data.append(entry)
        content = yaml.dump(data, sort_keys=False)

        pod_owner = get_pod_owner(repo, task_id)
        commit_and_log(
            repo,
            path,
            content,
            f"Append chain of thought to task {task_id}",
            task_id=task_id,
            committed_by=pod_owner
        )

        return {"message": "Chain of thought appended.", "appended_thought": entry}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Internal Server Error: {type(e).__name__}: {e}"})

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

    commit_and_log(repo, file_path, updated_yaml, f"Append handoff note to task {task_id}", task_id=task_id, committed_by=from_pod)

    return {"message": "Handoff note appended", "note": new_entry}

@app.post("/tasks/auto_generate_handoff/{task_id}")
async def auto_generate_handoff(task_id: str, repo_name: str = Body(...)):
    try:
        repo = get_repo(repo_name)
        note = generate_handoff_note(task_id, repo)
        return {"handoff_note": note}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to auto-generate handoff note: {str(e)}")


@app.post("/tasks/auto_handoff")
async def auto_handoff(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    next_task_id: str = Body(...),
    handoff_mode: Optional[str] = Body("async")
):
    repo = get_repo(repo_name)
    task_file = repo.get_contents("project/task.yaml")
    task_data = yaml.safe_load(task_file.decoded_content)

    if task_id not in task_data["tasks"] or next_task_id not in task_data["tasks"]:
        raise HTTPException(status_code=404, detail="One or both task IDs not found")

    task_data["tasks"][next_task_id]["handoff_from"] = task_id
    task_data["tasks"][next_task_id]["depends_on"] = [task_id]
    task_data["tasks"][next_task_id]["handoff_mode"] = handoff_mode
    task_data["tasks"][next_task_id]["status"] = "ready"

    updated_content = yaml.dump(task_data, sort_keys=False)
    commit_and_log(
        repo,
        "project/task.yaml",
        updated_content,
        f"Auto-handoff setup from {task_id} to {next_task_id}",
        task_id=task_id,
        committed_by="auto_handoff"
    )

    return {"message": f"Handoff from {task_id} to {next_task_id} configured."}

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

@app.post("/audit/validate_changelog")
async def validate_changelog(repo_name: str = Body(...), dry_run: bool = Body(default=False)):
    try:
        repo = get_repo(repo_name)
        task_file = repo.get_contents("project/task.yaml")
        tasks = yaml.safe_load(task_file.decoded_content).get("tasks", {})

        try:
            changelog_file = repo.get_contents("project/outputs/changelog.yaml")
            changelog = yaml.safe_load(changelog_file.decoded_content) or []
        except Exception:
            changelog = []

        # Map of output files per task
        expected_files = {}
        for tid, data in tasks.items():
            if data.get("done"):
                for f in data.get("outputs", []):
                    expected_files[f] = tid

        # Build set of logged paths
        logged_paths = set(entry["path"] for entry in changelog)

        # Check for missing changelog entries
        missing_entries = []
        for path, tid in expected_files.items():
            if path not in logged_paths:
                missing_entries.append({"task_id": tid, "path": path})

        # Commit missing entries using commit_and_log
        for entry in missing_entries:
            if dry_run:
                continue
            commit_and_log(
                repo,
                file_path=entry["path"],
                content="Backfilled entry placeholder",
                commit_message="Backfilled by changelog validator",
                task_id=entry["task_id"],
                committed_by="validator"
            )

        return {
            "missing_changelog_entries": missing_entries,
            "total_missing": len(missing_entries),
            "message": "Missing entries committed using commit_and_log."
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Validation error: {str(e)}"})


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
    handoff_note: Optional[dict] = Body(default={}),
    handoff_to_same_pod: Optional[bool] = Body(default=False),
    token_count: Optional[int] = Body(default=None)
):

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
        pod_owner = get_pod_owner(repo, task_id)   
        
        output_dir = f"project/outputs/{task_id}"
        output_paths = []
        for item in outputs:
            output_path = item["path"]
            output_content = item["content"]
            output_paths.append(output_path)
            commit_and_log(repo, output_path, output_content, f"Save output for {task_id}", task_id=task_id, committed_by=pod_owner)

        # Update outputs in task.yaml
        task_data["outputs"] = list(set(task_data.get("outputs", []) + output_paths))
        commit_and_log(repo, task_path, yaml.dump(task_data), f"Mark task {task_id} as completed and update outputs", task_id=task_id, committed_by=pod_owner)

        if reasoning_trace:
            trace_path = f"{output_dir}/reasoning_trace.yaml"
            commit_and_log(repo, trace_path, yaml.dump(reasoning_trace), f"Log reasoning trace for {task_id}", task_id=task_id, committed_by=pod_owner)

        # Auto-generate handoff if not provided
        if not handoff_note:
            handoff_note = generate_handoff_note(task_id, repo)

        if handoff_note:
            handoff_path = f"{output_dir}/handoff_notes.yaml"
            try:
                file = repo.get_contents(handoff_path)
                handoff_data = yaml.safe_load(file.decoded_content) or {}
            except:
                handoff_data = {}
            
            # Add scale flag if applicable
            if handoff_to_same_pod:
                handoff_note["handoff_type"] = "scale"
                if token_count:
                    handoff_note["token_count"] = token_count

            handoff_data.setdefault("handoffs", []).append(handoff_note)
            commit_and_log(repo, handoff_path, yaml.dump(handoff_data, sort_keys=False), f"Log handoff note for {task_id}", task_id=task_id, committed_by=pod_owner)

        return {"message": f"Task {task_id} completed and outputs committed."}

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})



@app.get("/tasks/{task_id}")
def get_task_details(task_id: str):
    task_data = fetch_yaml_from_github(file_path=TASK_FILE_PATH)
    tasks = task_data.get("tasks", {})

    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found.")

    return {"task_id": task_id, "metadata": tasks[task_id]}  

@app.post("/tasks/create")
async def create_new_task(
    repo_name: str = Body(...),
    phase: str = Body(...),
    task_key: str = Body(...),
    task_id: str = Body(...),
    assigned_pod: str = Body(...),
    prompt_variables: Optional[dict] = Body(default={})
):
    try:
        repo = get_repo(repo_name)
        task_path = "project/task.yaml"
        task_data = fetch_yaml_from_github(repo_name, task_path)

        if task_id in task_data.get("tasks", {}):
            raise HTTPException(status_code=400, detail=f"Task ID {task_id} already exists")

        # Load instance_of task template
        template_path = f"framework/task_templates/{phase}/{task_key}/task.yaml"
        task_template = fetch_yaml_from_github(repo_name, template_path)
        new_task = task_template.get("task", {})

        # Set metadata
        new_task["assigned_pod"] = assigned_pod
        new_task["created_at"] = datetime.utcnow().isoformat()
        new_task["updated_at"] = None
        new_task["done"] = False
        new_task["status"] = "backlog"
        new_task["instance_of"] = template_path
        new_task["prompt"] = f"framework/task_templates/{phase}/{task_key}/prompt_template.md"

        # Add to task list
        task_data.setdefault("tasks", {})[task_id] = new_task
        updated_yaml = yaml.dump(task_data, sort_keys=False)

        # Commit task.yaml
        commit_and_log(
            repo,
            file_path=task_path,
            content=updated_yaml,
            commit_message=f"Create new task {task_id} from template {task_key}",
            task_id=task_id,
            committed_by=assigned_pod
        )

        return {
            "message": f"Created new task {task_id} for pod {assigned_pod}.",
            "new_task_id": task_id,
            "task_metadata": new_task
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

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
        pod_owner = task.get("pod_owner", "Unknown")

        updated_yaml = yaml.dump(tasks)
        commit_and_log(repo, task_path, updated_yaml, f"Update metadata for {task_id}", task_id=task_id, committed_by=pod_owner)

        return {"message": "Task metadata updated", "task_id": task_id, "updated_task_metadata": task}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update metadata: {str(e)}")


# ---- Memory Management ----

@app.post("/memory/index")
async def index_memory(repo_name: str = Body(...), base_paths: Optional[List[str]] = None):
    try:
        repo = get_repo(repo_name)
        memory_path = "project/memory.yaml"
        try:
            memory_file = repo.get_contents(memory_path)
            memory = yaml.safe_load(memory_file.decoded_content) or []
        except Exception:
            memory = []

        memory_paths = set(entry.get("path") for entry in memory)
        base_paths = base_paths or []

        def recurse_files(path):
            entries = repo.get_contents(path)
            if not isinstance(entries, list):
                entries = [entries]
            for entry in entries:
                if entry.type == "file" and entry.path not in memory_paths:
                    content = repo.get_contents(entry.path).decoded_content.decode("utf-8")
                    meta = describe_file_for_memory(entry.path, content)
                    memory.append({
                        "path": entry.path,
                        "raw_url": entry.download_url,
                        "file_type": entry.name.split(".")[-1] if "." in entry.name else "unknown",
                        "description": meta["description"],
                        "tags": meta["tags"],
                        "last_updated": datetime.utcnow().date().isoformat(),
                        "pod_owner": meta["pod_owner"]
                    })
                elif entry.type == "dir":
                    recurse_files(entry.path)

        for base_path in base_paths:
            try:
                recurse_files(base_path)
            except Exception:
                continue

        memory_content = yaml.dump(memory, sort_keys=False)
        commit_and_log(repo, memory_path, memory_content, f"Indexed {len(memory)} memory entries", task_id="memory_index", committed_by="memory_indexer")

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

        new_entries = []
        for f in files:
            path = f["path"]
            try:
                file_content = repo.get_contents(path).decoded_content.decode("utf-8")
                meta = describe_file_for_memory(path, file_content)
                new_entries.append({
                    "path": path,
                    "raw_url": f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/{repo.name}/main/{path}",
                    "file_type": path.split(".")[-1] if "." in path else "unknown",
                    "description": meta["description"],
                    "tags": meta["tags"],
                    "last_updated": datetime.utcnow().date().isoformat(),
                    "pod_owner": meta["pod_owner"]
                })
            except Exception:
                continue

        memory.extend(new_entries)
        memory_content = yaml.dump(memory, sort_keys=False)

        commit_and_log(
            repo,
            file_path=memory_path,
            content=memory_content,
            commit_message=f"Add {len(new_entries)} entries to memory",
            task_id="memory_add",
            committed_by="memory_indexer"
        )

        return {"message": "New memory entries added", "memory_index": new_entries}
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
def get_metrics_summary(repo_name: str = Query(...)):
    summary = generate_metrics_summary(repo_name)
    reasoning_summary = generate_project_reasoning_summary(repo_name)
    summary["reasoning_summary"] = reasoning_summary

    # Write to metrics report file
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    metrics_path = f"project/outputs/reports/metrics_report_{timestamp}.yaml"
    metrics_content = yaml.dump(summary, sort_keys=False)

    commit_and_log(
        get_repo(repo_name),
        metrics_path,
        metrics_content,
        "Log project metrics report",
        task_id="metrics_summary",
        committed_by="MetricsBot"
    )

    return summary

@app.get("/metrics/export")
def export_metrics(repo_name: str = Query(...)):
    trace_paths = list_files_from_github(repo_name, REASONING_FOLDER_PATH)
    exported = []

    for path in trace_paths:
        if path.endswith("reasoning_trace.yaml"):
            try:
                trace = fetch_yaml_from_github(repo_name, path)
                exported.append({"task_id": trace.get("task_id", path.split("/")[-2]), **trace})
            except Exception:
                continue

    return {"entries": exported, "count": len(exported)}

# ---- Git Rollback ----

@app.post("/git/rollback_commit")
def rollback_commit(
    repo_name: str = Body(...),
    commit_sha: str = Body(...),
    paths: Optional[List[str]] = Body(default=None),
    reason: str = Body(default="Manual rollback")
):
    try:
        repo = get_repo(repo_name)
        commit = repo.get_commit(sha=commit_sha)
        files_to_revert = paths or [f.filename for f in commit.files]
        reverted_files = []

        for path in files_to_revert:
            history = repo.get_commits(path=path)
            target_version = None
            for c in history:
                if c.sha == commit_sha:
                    continue  # skip this commit
                target_version = c
                break

            if not target_version:
                continue

            contents = repo.get_contents(path, ref=target_version.sha)
            commit_and_log(
                repo,
                file_path=path,
                content=contents.decoded_content.decode(),
                commit_message=f"Rollback {path} to commit {target_version.sha}",
                task_id="rollback_commit",
                committed_by="RollbackBot"
            )
            reverted_files.append(path)

        # Log the rollback
        rollback_log_path = "project/.logs/reverted_commits.yaml"
        try:
            log_file = repo.get_contents(rollback_log_path)
            rollback_log = yaml.safe_load(log_file.decoded_content) or []
        except:
            rollback_log = []

        rollback_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "commit_sha": commit_sha,
            "paths": reverted_files,
            "reason": reason
        })

        log_content = yaml.dump(rollback_log, sort_keys=False)
        commit_and_log(
            repo,
            file_path=rollback_log_path,
            content=log_content,
            commit_message=f"Log rollback of {commit_sha}",
            task_id="rollback_commit",
            committed_by="RollbackBot"
        )

        return {
            "message": f"Rollback complete for {len(reverted_files)} files.",
            "reverted_files": reverted_files
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Rollback failed: {str(e)}"})

# ---- Scale Out When GPT Chat Reaches Limit ----

@app.post("/tasks/scale_out")
async def scale_out_task(
    repo_name: str = Body(...),
    task_id: str = Body(...),
    reason: Optional[str] = Body("Scaling due to context/token limits"),
    handoff_note: Optional[dict] = Body(default=None)
):
    try:
        repo = get_repo(repo_name)
        task_data = fetch_yaml_from_github(repo_name, "project/task.yaml")

        if task_id not in task_data.get("tasks", {}):
            raise HTTPException(status_code=404, detail=f"Task ID {task_id} not found.")

        original = task_data["tasks"][task_id]
        pod_owner = original.get("pod_owner", "UnknownPod")

        # Generate a new task ID with suffix _clone_N
        clone_index = 1
        while f"{task_id}_clone_{clone_index}" in task_data["tasks"]:
            clone_index += 1
        new_task_id = f"{task_id}_clone_{clone_index}"

        # Copy task and modify
        new_task = dict(original)
        new_task["status"] = "planned"
        new_task["done"] = False
        new_task["created_at"] = datetime.utcnow().isoformat()
        new_task["updated_at"] = None
        new_task["handoff_from"] = task_id
        new_task["description"] = f"Scale-out clone of {task_id}"
        new_task["notes"] = reason

        task_data["tasks"][new_task_id] = new_task
        updated_yaml = yaml.dump(task_data, sort_keys=False)

        commit_and_log(
            repo,
            file_path="project/task.yaml",
            content=updated_yaml,
            commit_message=f"Scale out task {task_id} to {new_task_id}",
            task_id=new_task_id,
            committed_by=pod_owner
        )

        # Use provided handoff_note or generate default
        if not handoff_note:
            handoff_note = {
                "timestamp": datetime.utcnow().isoformat(),
                "from_pod": pod_owner,
                "to_pod": pod_owner,
                "reason": reason,
                "handoff_type": "scale",
                "reference_files": original.get("outputs", []),
                "notes": f"GPT reached context/token limit on {task_id}. Work handed off to {new_task_id}.",
                "ways_of_working": "Resume mid-task using prior context"
            }

        # Store handoff note
        handoff_path = f"project/outputs/{task_id}/handoff_notes.yaml"
        try:
            handoff_file = repo.get_contents(handoff_path)
            handoff_data = yaml.safe_load(handoff_file.decoded_content) or {}
        except:
            handoff_data = {}

        handoff_data.setdefault("handoffs", []).append(handoff_note)
        commit_and_log(
            repo,
            file_path=handoff_path,
            content=yaml.dump(handoff_data, sort_keys=False),
            commit_message=f"Log scale handoff from {task_id} to {new_task_id}",
            task_id=task_id,
            committed_by=pod_owner
        )

        return {
            "message": f"Created new scale-out task {new_task_id}",
            "new_task_id": new_task_id,
            "task_metadata": new_task,
            "next_step": f"Call /tasks/start with task_id: {new_task_id} to continue work.",
            "inputs": new_task.get("inputs", []),
            "prior_outputs": original.get("outputs", []),
            "handoff_note": handoff_note
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": str(e)})

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
            if method.lower() not in ["get", "post", "put", "patch", "delete"]:
                continue

            tags = details.get("tags", ["General"])
            for tag in tags:
                if tag not in grouped_actions:
                    grouped_actions[tag] = []

                action_name = details.get("x-gpt-action", {}).get("name", details.get("summary", f"{method.upper()} {path}"))
                action_description = details.get("description") or details.get("summary", "")
                grouped_actions[tag].append({
                    "name": action_name,
                    "path": path,
                    "method": method.upper(),
                    "description": action_description
                })

    actions_response = []
    for tag, actions in grouped_actions.items():
        actions_response.append({
            "category": tag,
            "tools": actions
        })

    return {"actions": actions_response}

@app.post("/system/guide")
def get_onboarding_guide(
    repo_name: str = Body(...),
    simple: bool = Body(default=False)
):
    """Returns either the technical or simplified onboarding guide from GitHub."""
    try:
        repo = get_repo(repo_name)
        filename = "project/docs/onboarding_guide_simple.md" if simple else "project/docs/onboarding_guide.md"
        guide_file = repo.get_contents(filename)
        content = guide_file.decoded_content.decode("utf-8")
        return PlainTextResponse(content, media_type="text/markdown")
    except Exception as e:
        return JSONResponse(status_code=500, content={"detail": f"Failed to retrieve guide: {str(e)}"})