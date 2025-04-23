# ✅ Patch: AI-Native Task Management – Multi-Pod Enablement

This patch defines all necessary scripts, schema, and updates to implement a multi-pod, AI-native task execution and orchestration model using DeliveryPod GPT and FastAPI.

---

## 📁 Scripts Required for the Framework

| Script | Role |
|--------|------|
| `init_project_tasks.py` | Seed `tasks.yaml` from `task_templates/` |
| `select_tasks_for_sprint.py` | Create `sprint.yaml` subset for sprint planning |
| `activate_next_task.sh` | Move one or more tasks from `sprint.yaml` to `active_tasks/` |
| `generate_patch_from_output.sh` | Generates patch from GPT output and promotes it via `--task_file` |
| `create_pr_from_patch.sh` | Applies patch, commits, pushes, and opens PR |
| `complete_task.sh` | Marks task `done: true`, updates timestamp, optionally archives completed task file |
| `sync_memory.py` | Update memory.yaml with any finalized output paths from task.yaml |

---

## 🧠 FastAPI Patch for Task Operations

Below are the FastAPI route implementations to support the task flow:

```python
# main.py
from fastapi import FastAPI, HTTPException, Body
import os
import requests
import base64
from pathlib import Path
import yaml
import json
from typing import List, Dict

app = FastAPI()

GITHUB_API = "https://api.github.com"
REPO = "stewmckendry/ai-concussion-agent"
BRANCH = "main"


def read_yaml_from_github(path):
    url = f"{GITHUB_API}/repos/{REPO}/contents/{path}?ref={BRANCH}"
    headers = {"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}", "Accept": "application/vnd.github+json"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    content = base64.b64decode(res.json()["content"]).decode()
    return yaml.safe_load(content)

def list_github_directory(path, github_api, repo, branch):
    import requests
    url = f"{github_api}/repos/{repo}/contents/{path}?ref={branch}"
    response = requests.get(url)
    response.raise_for_status()
    return [item["name"] for item in response.json() if item["type"] == "dir"]



@app.post("/init_tasks")
def init_tasks():
    PHASES = list_github_directory("task_templates", GITHUB_API, REPO, BRANCH)

    steps = []
    for phase in PHASES:
        try:
            phase_steps = list_github_directory(f"task_templates/{phase}", GITHUB_API, REPO, BRANCH)
            steps.extend((phase, step) for step in phase_steps)
        except Exception as e:
            print(f"⚠️ Failed to list {phase}: {e}")

    backlog = {"tasks": {}}
    for phase in PHASES:
        for step in steps:
            try:
                path = f"task_templates/{phase}/{step}/task.yaml"
                try:
                    content = read_yaml_from_github(path)
                    stripped = yaml.safe_load("
".join(str(content).split("
")[2:]))  # remove header and blank line
                    backlog["tasks"].update(stripped.get("tasks", {}))
                backlog["tasks"].update(data.get("tasks", {}))
            except Exception as e:
                print(f"⚠️ Failed to load {phase}/{step}: {e}")

    with open("tasks.yaml", "w") as f:
        yaml.dump(backlog, f)
    return {"tasks_created": list(backlog["tasks"].keys())}

@app.get("/get_sprint_planning_tasks")
def get_sprint_planning_tasks():
    tasks = {"project": {}, "sprint": {}}
    all_tasks = read_yaml_from_github("tasks.yaml").get("tasks", {})
    for tid, t in all_tasks.items():
        if t.get("status") in ["pending", "todo"]:
            tasks["project"][tid] = t
    try:
        sprint_tasks = read_yaml_from_github("sprint.yaml").get("tasks", {})
        tasks["sprint"] = sprint_tasks
    except Exception:
        pass
    return tasks

@app.post("/plan_sprint")
def plan_sprint(task_ids: List[str] = Body(...)):
    try:
        backlog = read_yaml_from_github("tasks.yaml")["tasks"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unable to retrieve tasks.yaml: {e}")

    try:
        current_sprint = read_yaml_from_github("sprint.yaml").get("tasks", {})
    except Exception:
        current_sprint = {}

    sprint = {"tasks": {tid: backlog[tid] for tid in task_ids if tid in backlog}}
    return sprint

@app.post("/activate_task")
def activate_task(task: Dict):
    task_id = task["task_id"]
    try:
        existing_task = read_yaml_from_github(f"active_tasks/{task_id}.yaml")
    except Exception:
        existing_task = {}

    updated_task = {**existing_task, **task}
    return {"updated_task": updated_task}

@app.get("/get_active_tasks")
def get_active_tasks():
    task_files = list_github_directory("active_tasks", GITHUB_API, REPO, BRANCH)

    active = []
    active_by_pod = defaultdict(list)
    for filename in task_files:
        item_path = f"active_tasks/{filename}"
        task = read_yaml_from_github(item_path)
        task = read_yaml_from_github(item["path"])
        task_info = {
            "task_id": filename.replace(".yaml", ""),
            "assigned_pod": task.get("assigned_pod", "Unassigned"),
            "status": task.get("status", "unknown"),
            "summary": task.get("description", ""),
            "updated_at": task.get("updated_at", "")
        }
        active.append(task_info)
                active_by_pod[task_info["assigned_pod"]].append(task_info)

    sprint = {}
    try:
        sprint = read_yaml_from_github("sprint.yaml").get("tasks", {})
    except Exception:
        pass

    total_sprint_tasks = len(sprint)
    completed = sum(1 for t in sprint.values() if t.get("done") is True)
    in_progress = len(active)
    remaining = total_sprint_tasks - completed - in_progress

    progress = {
        "total": total_sprint_tasks,
        "completed": completed,
        "in_progress": in_progress,
        "remaining": max(0, remaining)
    }

    def get_phase(t):
        return t.get("phase", "Z")

    sprint_sorted = dict(sorted(sprint.items(), key=lambda item: get_phase(item[1])))

    return {
        "progress": progress,
        "sprint_plan": sprint_sorted,
        "active_by_pod": dict(active_by_pod)
    }





@app.get("/get_prompt")
def get_prompt(task_id: str = Body(...)):
    try:
        all_tasks = read_yaml_from_github("tasks.yaml")["tasks"]
        task = all_tasks[task_id]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Task not found in tasks.yaml: {e}")

    prompt_path = task.get("prompt")
    if not prompt_path:
        raise HTTPException(status_code=400, detail="Prompt path not defined in task")

    try:
        prompt_file = read_yaml_from_github(prompt_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading prompt: {e}")

    # Validate required inputs exist in memory.yaml
    try:
        memory = read_yaml_from_github("memory.yaml")
        missing_inputs = [f for f in task.get("inputs", []) if not any(m.get("path") == f for m in memory.get("files", []))]
    except Exception:
        missing_inputs = task.get("inputs", [])

    return {
        "task_id": task_id,
        "prompt": prompt_file,
        "missing_inputs": missing_inputs
    }




```

---
