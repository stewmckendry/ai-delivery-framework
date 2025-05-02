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
