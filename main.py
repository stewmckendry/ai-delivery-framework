# 📁 github_proxy/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pathlib import Path
import httpx, os, json
from dotenv import load_dotenv
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List


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

# ---- New Promote Patch Tool ----

class PromotePatchInput(BaseModel):
    task_id: str
    summary: str
    output_folders: List[str]
    diff: str  # ✅ real patch content from GPT

class PromotePatchOutput(BaseModel):
    patch_file: str
    task_id: str
    summary: str
    output_folders: List[str]
    download_url: str  # URL for downloading the patch diff file
    metadata_url: str  # ✅ New! URL for downloading the metadata JSON file

class ValidateDiffInput(BaseModel):
    diff: str

@app.post("/promote_patch", response_model=PromotePatchOutput)
def promote_patch(data: PromotePatchInput):
    patch_file = f"patch_{data.task_id}.diff"
    json_file = patch_file.replace(".diff", ".json")

    patch_dir = Path("/mnt/data/.patches")
    patch_dir.mkdir(parents=True, exist_ok=True)
    patch_path = patch_dir / patch_file
    patch_path.write_text(data.diff)

    meta = {
        "patch_file": patch_file,
        "task_id": data.task_id,
        "summary": data.summary,
        "output_folders": data.output_folders
    }

    json_path = patch_dir / json_file
    json_path.write_text(json.dumps(meta, indent=2))

    base_url = "https://ai-concussion-agent-production.up.railway.app/patches"
    return {
        "patch_file": patch_file,
        "task_id": data.task_id,
        "summary": data.summary,
        "output_folders": data.output_folders,
        "download_url": f"{base_url}/{patch_file}",
        "metadata_url": f"{base_url}/{json_file}"
    }

@app.post("/validate_diff")
def validate_diff(data: ValidateDiffInput):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp_file:
        tmp_file.write(data.diff)
        tmp_file.flush()

        try:
            subprocess.run(["git", "apply", "--check", tmp_file.name], check=True, capture_output=True)
            return {"valid": True, "message": "Patch is valid."}
        except subprocess.CalledProcessError as e:
            return {"valid": False, "message": e.stderr.decode()}

@app.get("/patches/{patch_name}")
def get_patch_file(patch_name: str):
    patch_path = Path("/mnt/data/.patches") / patch_name
    if patch_path.exists():
        return FileResponse(patch_path, media_type="text/plain", filename=patch_name)
    else:
        raise HTTPException(status_code=404, detail="Patch not found")
    
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
