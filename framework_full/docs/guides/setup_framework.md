# 🛠 Setting Up the AI-Native Delivery Framework

This guide helps you deploy the full FastAPI server, connect it to GitHub, configure memory systems, and validate the first project run.

---

# 1. Prerequisites

✅ GitHub Repo Created  
✅ Railway / AWS / Azure account for API hosting  
✅ GitHub Personal Access Token (PAT)  
✅ Docker (optional if self-hosting)  

---

# 2. System Components to Set Up

| Component | Description |
|:---|:---|
| FastAPI Server | Hosts task, memory, patch, and metrics APIs |
| GitHub Repo | Stores tasks, memory, reasoning, patches |
| Custom GPTs | Connect to API actions for Pod operations |
| Local Dev Environment (optional) | Test API endpoints before production use |

---

# 3. Step-by-Step Setup

### Step 1: Clone the Framework Repo

```bash
git clone https://github.com/{your-org}/{framework-repo}.git
cd framework-repo
```

---

### Step 2: Deploy the API

**Option 1: Railway (Recommended Quick Start)**

1. Create a new project
2. Link GitHub repo
3. Set environment variables:
   - `GITHUB_OWNER={your-org}`
   - `GITHUB_REPO={your-project-repo}`
   - `GITHUB_BRANCH=main`
   - `GITHUB_TOKEN={your PAT}`

4. Deploy!

**Option 2: Self-Host with Docker**
```bash
docker build -t ai-delivery-api .
docker run -e GITHUB_OWNER=... -e GITHUB_REPO=... -p 8000:8000 ai-delivery-api
```

---

### Step 3: Validate API Access

Open:
```
https://{your-api-host}/docs
```
Test:
- `/tasks/list`
- `/memory/search`
- `/patches/promote`

---

### Step 4: Configure Custom GPT

In OpenAI:
- Create a Custom GPT
- Set Authentication to Bearer Token
- Set Base URL to your FastAPI server
- Import actions from:
  ```
  https://{your-api-host}/openapi.json
  ```

---

### Step 5: Confirm Full Flow

✅ Pod activates task  
✅ Fetches memory  
✅ Promotes patch  
✅ No manual scripts needed

---

# 4. Success Checklist

✅ FastAPI live at public URL  
✅ GitHub repo connected and writable  
✅ Custom GPT can call task/memory/patch actions  
✅ Pilot tasks activated and completed  

---

# 5. Example Env Vars for Hosting

```bash
GITHUB_OWNER=stewmckendry
GITHUB_REPO=ai-delivery-framework
GITHUB_BRANCH=main
GITHUB_TOKEN=your_pat_here
```

---

# 6. Troubleshooting

| Symptom | Cause | Fix |
|:---|:---|:---|
| 401 Unauthorized | Bad GitHub token | Check token scopes |
| 500 API Errors | API server misconfigured | Review logs |
| Task list empty | No task.yaml pushed yet | Add sample tasks |

---

# 🏁 You're now fully deployed and ready to onboard Pods!
