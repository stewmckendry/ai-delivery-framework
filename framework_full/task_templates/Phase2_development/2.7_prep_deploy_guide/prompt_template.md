### 2.7 Prompt Template

```markdown
🎯 POD MISSION: DevPod – Prepare Deployment Guide

🧾 TASK YAML:
task_id: 2.8_prepare_deployment_guide  
pod: DevPod  
description: Create a guide to deploy the current feature set to a test, staging, or production environment, including all steps, configs, and dependencies

📁 MEMORY:
- path: docs/specs/spec_<feature_id>.md  
  repo: stewmckendry/ai-delivery-framework  
- path: .patches/patch_<timestamp>.diff  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool to retrieve:
- The finalized feature spec  
- The latest patch diff  
- Any notes on environment or infra config from earlier phases

---

### ✅ Deployment Guide Instructions

1. **Summarize Feature Deployment Context**
   - State what feature(s) this guide supports  
   - Note if this is for testing, staging, or production deployment

2. **Document Environment and Dependencies**
   - Required environment(s): `dev`, `test`, `prod`, etc.  
   - Dependencies: Python version, models, packages, container base image  
   - System-level requirements: Docker, Git, Python, etc.  
   - Required services: API keys, external tools, vector DBs, etc.

3. **List Environment Variables and Secrets**
   - Include all required env vars  
   - Label sensitive variables as `[SECRET]`  
   - Point to `.env.example` or secret manager config if applicable

4. **Define Deployment Steps**
   - **Manual Steps**:
     - Clone repo, activate env, install dependencies  
     - Run init scripts, migrations, or tests  
     - Deploy using Docker, Streamlit, FastAPI, etc.  
   - **CI/CD Steps**:
     - Trigger GitHub Action or pipeline  
     - Reference `.github/workflows/deploy.yaml` or equivalent  
     - Describe how to monitor deployment logs

5. **Include Post-Deployment Validation**
   - How to confirm deployment success (e.g., health checks, smoke tests)  
   - Where to check logs or outputs  
   - Who to notify

---

### 📥 Save Final Guide

✅ Save completed guide to:  
`docs/deployment/deployment_guide.md`

Include structured sections:
#Deployment Guide
##Feature Summary
##Environments
##Dependencies
##Environment Variables
##Deployment Steps (Manual & CI)
##Post-Deployment Checks
##Troubleshooting
---

📌 Final Notes:
- Tag any blockers or assumptions in the guide using `> [GAP]` or `> [FOLLOW-UP]`  
- If major deployment infrastructure is missing or unclear, suggest a ResearchPod spike  
- Add deployment status summary to the feedback file
```
