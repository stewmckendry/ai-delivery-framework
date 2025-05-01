## ✅ Publishing a Safe, Public ProductPod GPT

### 🎯 Goal
Enable external users to safely explore the AI-native delivery framework using a public-facing ProductPod Custom GPT, while ensuring sandboxed, auditable Git access and clear onboarding.

---

### 🚧 Key Constraints and Solutions

| Challenge                              | Solution                                                                 |
|----------------------------------------|--------------------------------------------------------------------------|
| No GPT user-specific auth              | Require repo_name and repo_owner, validate fork in backend              |
| Risk of shared repo overwrites         | Force writes to forked repo or sandbox branches                         |
| Risky tool exposure                    | Expose only safe, read/write-limited tools                              |
| New user onboarding                    | Provide clear guide via GPT system message and markdown link            |

---

### 🔧 Architecture Plan

#### 1. Custom GPT: ProductPod Sandbox GPT
- **Hosted on:** OpenAI GPT Builder
- **Actions exposed via:** OpenAPI schema (FastAPI)
- **Safe tool list only:**
  - `GET /tasks/list`
  - `POST /tasks/start`
  - `GET /memory/search`
  - `GET /tasks/fetch_reasoning_trace`
  - `POST /tasks/commit_and_log_output`
  - `GET /tasks/artifacts`

#### 2. Git Strategy: Per-User Sandbox
- **Preferred option:** Ask each user to fork `ai-delivery-framework`
- **Alternative:** Require branch per user: `sandbox-{username}`
- **Backend logic (in sandbox_validator.py):**
  - Reject unauthorized writes (e.g., to main)
  - Confirm fork status via GitHub API
  - Require `repo_owner` + `repo_name` in POSTs

#### 3. FastAPI Hardening
- ✅ Validate all repo inputs
- ✅ Restrict toolset by role or GPT name
- ✅ Add RBAC logic to reject disallowed routes
- ✅ (Optional) Log tool access per request

---

### 📘 Welcome Guide for GPT

```markdown
## 👋 Welcome to ProductPod Sandbox GPT

You’re about to explore an AI-native delivery system backed by Git + reasoning.

### 🔧 Setup Steps
1. Fork the base repo: [ai-delivery-framework](https://github.com/YOUR_ORG/ai-delivery-framework)
2. Rename as: `ai-delivery-framework-{yourname}`
3. Provide your GitHub username and repo name when prompted

### ✅ What You Can Do
- View tasks and memory
- Start and log a task
- Commit outputs and thoughts to your fork
- Review what GPT (or others) did

### 🛑 What You Can’t Do
- No writes to shared repo
- No destructive actions
- No access to admin tools

All reasoning is logged in your fork, traceable and safe.
```

---

### 📊 Optional: Usage Monitoring
- Track by `repo_owner`
- Log tool usage frequency
- Add `/metrics/sandbox_activity`

---

### 🧪 Summary Plan

| Step                     | What to Do                                                            |
|--------------------------|-----------------------------------------------------------------------|
| ✅ Create GPT            | Point to FastAPI OpenAPI schema                                       |
| ✅ Expose Safe Tools     | Use OpenAPI filter or backend RBAC                                    |
| ✅ Enforce Git Safety    | Require forks/branches, use sandbox_validator.py                      |
| ✅ Add Onboarding Msg    | In system prompt + markdown welcome guide                             |
| ✅ Monitor Usage         | (Optional) Log calls, repo_owner, tool usage metrics                  |

---

Would you like example code for the `sandbox_validator.py` logic or a production-ready OpenAPI fragment for tool restriction?

