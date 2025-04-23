# 📁 github_proxy/main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import FileResponse
from pathlib import Path
import httpx, os, json
from dotenv import load_dotenv

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

class PromotePatchOutput(BaseModel):
    patch_file: str
    task_id: str
    summary: str
    output_folders: List[str]

@app.post("/promote_patch", response_model=PromotePatchOutput)
def promote_patch(data: PromotePatchInput):
    # Simulated patch path (real version would run diff + save .patch file)
    patch_file = f".patches/patch_simulated_{data.task_id}.diff"
    return {
        "patch_file": patch_file,
        "task_id": data.task_id,
        "summary": data.summary,
        "output_folders": data.output_folders
    }

@app.get("/patches/{patch_name}")
def get_patch_file(patch_name: str):
    patch_path = Path(".patches") / patch_name
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
