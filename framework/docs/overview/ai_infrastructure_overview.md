# ✍️ Your Own Private AI Workshop (Non-Technical Version)

## 🚀 Mission

We're building a **creative workshop for builders** — a space where anyone can collaborate with an AI to build apps, manage delivery, and organize their thinking.

But we know how risky it can feel to “let go” and allow AI to write code or modify your repo. That’s why we’ve made sure every workspace is **safe, isolated, and reversible**.

---

## 🧩 The Solution

Everyone who tries our framework gets their own **sandbox branch** — a private, safe workspace inside GitHub.

Think of it like your **digital drafting room**:
- You and the AI work freely.
- The `main` branch stays untouched — unless *you* decide to merge.
- Everything is **logged, backed up, and undoable**.

You can come back anytime using your secure token and pick up where you left off.

---

## 🛠️ How It Works

When you chat with our GPT-based tools:

- ✅ A **private branch** is created for you (e.g., `sandbox-golden-eagle`)
- 🔐 You get a **token** to return to your space later
- 🧠 You build, write, and explore safely in that branch
- 🔄 You can **undo** any change or return to `main` anytime
- 📤 When ready, you can **publish or merge** your work

---

## 📖 How to Get Started

Just start a conversation with our Custom GPT — it will walk you through:

- Creating your **private branch**
- Naming your **project**
- Setting **goals**
- Using tools like:
  - 📝 File editors  
  - ✅ Task trackers  
  - 💬 Prompt builders

No installation. No pressure. No risk.

---

# 👩‍💻 Branch-Isolated AI Workspaces with Audit + Rollback (Technical Version)

## 🎯 Goal

Enable **safe, concurrent, and trackable** AI interaction with GitHub repos — using GPT + OpenAPI-based tools — while protecting mainline stability and user trust.

---

## 🧱 Stack

- **FastAPI** backend (hosted on Railway)
- **OpenAPI schema** with Custom GPT tool integration
- **GitHub API** via PyGithub with Personal Access Token (PAT)
- Each GPT call includes `repo_name` and `branch`

Tools support the **full app delivery lifecycle**:
- Create tasks
- Log reasoning
- Commit files
- Rollback changes

---

## 🛡️ Core Features

| Feature               | Details                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| Sandboxed Branching   | Each user gets a branch like `sandbox-velvet-puma`                      |
| Branch Reuse Token    | GPT returns a token that maps securely back to the user’s branch        |
| Safe Commits          | All file changes use `commit_and_log()` with metadata + changelog       |
| Rollback Tool         | Undo any commit by SHA with logging to `.logs/reverted_commits.yaml`    |
| Tool Param Standardization | All tools accept `repo_name` and `branch`, OpenAPI-documented    |
| Query Throttling      | Pagination added to `/memory/query` to prevent token overflow           |
| Unified Init Tool     | `/sandbox/init` with `mode: branch` or `mode: project`                  |

---

## 🧪 Developer Flow

1. **Init**  
   Call `/sandbox/init` with `mode: branch`  
   → creates or reuses a unique branch

2. **Setup**  
   Optionally call `/sandbox/init` with `mode: project`  
   → scaffolds `memory.yaml`, `task.yaml`, `reasoning_trace.md`

3. **Work**  
   Use tools to:
   - Edit files
   - Track tasks
   - Log thoughts  
   → all scoped to your private branch

4. **Undo**  
   Use `/git/rollback_commit` if needed

5. **Export or Merge**  
   Use `/system/metrics` to summarize  
   → Push to `main` manually when ready

---

## 🧠 GPT Prompt Design

- Every GPT response includes the current `repo_name` and `branch`
- Users are reminded to **save their `reuse_token`**
- GPT tools **always pass the branch** in every API call

---

# 🪜 Infrastructure Maturity Plan

A human-first explanation of how we scale the AI Delivery Framework — from single-user sandboxes to enterprise-ready platforms.

---

## 🪜 PHASE 1: Harden the Sandbox *(Where We Are Now)*

### 🧠 What It Is

This phase ensures **every user has a safe, private space** to work with the AI — without affecting others, losing data, or damaging the core repo.

### 🔧 Key Concepts

- **Branch Isolation**  
  Every user works in their own Git branch (e.g., `sandbox-golden-fox`).  
  _Like giving each person a separate copy of the whiteboard._

- **Token-Based Resume**  
  Each branch has a unique token so users can return to it later.  
  _Think of it as a room key._

- **Audit + Rollback**  
  Every change is logged and reversible.

### 🛠 Why It Matters

It gives people **confidence to experiment** and gives you **peace of mind** that the AI won’t wreck anything.  
_It’s like putting bumpers on a bowling lane._

---

## 🪜 PHASE 2: Multi-Org Readiness

### 🧠 What It Is

Once individuals succeed, the next step is to support **teams and organizations**:

- Each team has its own space  
- Data is isolated  
- Access is scoped to the right people

### 🔧 Key Concepts

- **Org Routing**  
  Let orgs or projects be uniquely identified (`acme-ml`, `beta-lab`)

- **GitHub App Tokens**  
  Replace shared tokens with scoped GitHub App installs — more secure

- **Private Repo Access**  
  Support credentials and token storage per org/project

### 🛠 Why It Matters

Now you can **invite other companies to use the framework** safely.  
_It’s the difference between a public demo and a private beta._

---

## 🪜 PHASE 3: Infrastructure Ops & Monitoring

### 🧠 What It Is

As usage scales, you need to see what’s happening and **respond to issues**.  
_This is your dashboard and control panel._

### 🔧 Key Concepts

- **Admin Console**  
  See which branches, users, or tools are active

- **Error Logging**  
  Be notified when GPT calls fail or commits break

- **GitHub Webhooks**  
  Sync human-made changes back into GPT memory (`memory.yaml`)

### 🛠 Why It Matters

You gain **visibility and control at scale** — to support many teams without flying blind.

---

## 🪜 PHASE 4: Ecosystem and Extensions

### 🧠 What It Is

This transforms the framework into a true **platform** others can build on.

### 🔧 Key Concepts

- **Templates Marketplace**  
  Starter kits for common use cases (e.g., LLM chatbot)

- **Custom Tools API**  
  Let others build and plug in their own GPT tools

- **Versioning**  
  Manage tool updates over time (like packages in NPM)

- **Audit Compliance**  
  Store trace logs for SOC2, GDPR, or internal audits

### 🛠 Why It Matters

It makes the AI Delivery Framework **adaptable and enterprise-ready** — a platform, not just a product.


---

# 🪜 Infrastructure Maturity Plan: Phase Matrix

---

## 🪜 PHASE 1: Harden the Sandbox *(✓ Experimental → Reliable)*

🎯 **Goal:** Let anyone experiment safely with AI in their own Git space

| ✅ What We Have Now                             | 🔧 What We Need to Build                                  |
|--------------------------------------------------|------------------------------------------------------------|
| Branch isolation for each GPT user (`sandbox-*`) | Limit access to assigned branch only (system/GPT-enforced) |
| Reuse token for returning to same branch         | Optional TTL or soft expiration for tokens                |
| All tools accept `branch` and `repo_name`        | Add fallback/default handling for missing `branch` param   |
| Commit + changelog + `memory.yaml` integration   | Alert/log when file changes fail silently                 |
| Rollback tool with commit SHA support            | Improve UI/log visibility for rollback results             |

---

## 🪜 PHASE 2: Multi-Org Readiness *(✓ Single-user → Org-safe)*

🎯 **Goal:** Support multiple users, teams, or companies safely

| ✅ What We Have Now                             | 🔧 What We Need to Build                                        |
|--------------------------------------------------|------------------------------------------------------------------|
| GitHub token scoped to a single user's repos     | Switch to GitHub App auth (per org/session)                     |
| Users can specify `repo_name` manually           | Org-aware repo routing (`org-user-ml`)                          |
| All GPT sessions are logically isolated          | Enforce physical isolation via per-org repos                    |
| GPT prompt includes `branch` and token           | Support org-aware token enforcement                             |

---

## 🪜 PHASE 3: Infrastructure Ops & Observability

🎯 **Goal:** Operate and monitor the platform at scale

| ✅ What We Have Now                            | 🔧 What We Need to Build                                        |
|--------------------------------------------------|------------------------------------------------------------------|
| Metrics export tool for reasoning traces        | Admin dashboard with branch/project statistics                 |
| Memory query tools (`search`, `list`, `stats`)  | Alerting/logging for failed GPT/tool executions                |
| Changelog and `task.yaml` tracked in Git        | GitHub Webhooks to sync human-made changes                     |
| Task lifecycle tool for project delivery        | Usage rate limits, quota enforcement, token abuse detection    |

---

## 🪜 PHASE 4: Ecosystem + Extension Framework

🎯 **Goal:** Make the framework reusable, extensible, and enterprise-ready

| ✅ What We Have Now                              | 🔧 What We Need to Build                                             |
|---------------------------------------------------|-----------------------------------------------------------------------|
| Project init + prompt bootstrapping tools         | Templates marketplace (starter kits, prompt packs)                   |
| Unified OpenAPI spec for GPT tools                | Versioning support (e.g., tool schema v1, v2 compatibility)          |
| All actions logged via `commit_and_log()`         | Exportable audit trail (e.g., JSON/CSV log format)                   |
| Rollback + changelog diff support                 | Compliance hooks (e.g., GDPR, SOC2 audit log integration)            |

