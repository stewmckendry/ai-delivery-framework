# 📁 github_proxy/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pathlib import Path
import httpx, os, json, re
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict
import tempfile
import yaml
import requests
import zipfile
from datetime import datetime

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

@app.post("/tasks/update-metadata")
def update_task_metadata(req: TaskUpdateRequest):
    """
    Updates fields in task.yaml for the given task_id.
    Returns the updated task.yaml contents (as text) — GPT will handle patch packaging.
    """
    # 🔄 Load task.yaml from GitHub
    data = fetch_task_yaml_from_github()

    task_id = req.task_id
    tasks = data.get("tasks", {})

    if task_id not in tasks:
        raise HTTPException(status_code=404, detail=f"Task '{task_id}' not found")

    # 🔧 Apply updates
    for key, value in req.fields.items():
        tasks[task_id][key] = value
    tasks[task_id]["updated_at"] = datetime.now().isoformat()

    # 🔁 Return updated YAML string (not file download)
    updated_yaml_str = yaml.dump(data, sort_keys=False)
    return JSONResponse(content={"task_id": task_id, "task_yaml": updated_yaml_str})


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
