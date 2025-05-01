## ✅ Correct Flow for Starting a Task

---

### 🧠 What Happens

1. **User or GPT calls** `/tasks/next` or `/tasks/activate` to retrieve a task.
2. The returned task includes a pointer to `prompt_template`, which the human uses to craft the actual prompt.
3. **User edits the prompt**, then starts the task by calling:

POST /tasks/start  
{
  "repo_name": "...",
  "task_id": "...",
  "prompt_used": "🧠 Full prompt content actually sent to GPT"
}

---

### ✅ System Actions in `/tasks/start`

- Marks the task as `in_progress`
- Saves `prompt_used.txt` under:  
  `project/outputs/<task_id>/`
- Optionally logs the path to this prompt in `task.yaml` (`prompt_used`)
- **Does not return** the prompt content — caller already has it

---

### ✅ Required Fixes to Current Patch

Current implementation of `/tasks/start` still includes:

# Load optional prompt content (template)  
prompt_template_path = task.get("prompt")  
...  
prompt_content = "Prompt file missing."  
...  
# returned in response  
"prompt_content": prompt_content

🛠 **This logic is outdated and must be removed.**

---

### 🔧 Patch Plan: Simplify `/tasks/start`

**Remove:**
- Any fetching or returning of the prompt template file

**Keep:**
- Saving `prompt_used.txt`
- Recording `prompt_used` path in `task.yaml`


## ✅ (1) Output File Scenarios: Task → Changelog Flow

### 🟢 Scenario A: Happy Path — Standard Task Completion

| Step | Owner | Tool | Purpose |
|------|-------|------|---------|
| 1. /tasks/start | GPT or Human | Returns prompt, inputs, handoff note | Start work with context |
| 2. Reasoning + work | GPT Pod | /tasks/append_chain_of_thought | Iterative thoughts saved |
| 3. Submit outputs | GPT Pod | /tasks/complete | Saves output files, updates task.yaml.outputs, logs reasoning_trace.yaml |
| 4. Commit | Auto via `commit_and_log` | — | Updates changelog.yaml with task ID, file path, timestamp, and rationale |

📌 **Use Case:** This is the ideal flow for traceability — every file written is trace-linked to a task.

---

### 🟡 Scenario B: Reopen and Re-complete a Task

| Step | Owner | Tool | Purpose |
|------|-------|------|---------|
| 1. /tasks/start again | Human or GPT | — | Resumes an existing task |
| 2. Submit new output(s) | GPT or Human | /tasks/complete (again) | Appends additional files or replaces old ones |
| 3. Changelog | Auto via `commit_and_log` | — | Adds new file entries or updated versions with new timestamp and reason |

📌 **Use Case:** When more work is required on the same task (e.g., feedback, missed edge case, follow-up test).

---

### 🔴 Scenario C: Manual Changes Outside Lifecycle (Backdoor Patch)

| Step | Owner | Tool | Purpose |
|------|-------|------|---------|
| 1. File updated manually | Human via Git CLI or GitHub UI | — | Not tied to task |
| 2. Changelog not updated | — | — | File appears in repo but not in changelog.yaml |
| 3. Run /audit/validate_changelog | Human | — | Scans all task.yaml[outputs] vs changelog.yaml |
| 4. Auto-fix | Human-approved | Tool | Adds missing entries using fallback reasoning (file path, task description, commit msg) |

📌 **Use Case:** Quick fix during debugging, fast iteration, or recovering from a crash when calling /complete wasn’t feasible.

---

### 🧠 Summary Table

| Scenario | Task-linked | Tools Used | Audit Trust | Typical Use |
|----------|-------------|------------|-------------|-------------|
| A: Happy Path | ✅ | start, complete | ✅ Clean audit trail | Normal flow |
| B: Reopen Task | ✅ | start, complete (again) | ✅ Trust maintained | Iterative update |
| C: Manual Edit | ❌ (at first) | Git only, then validate | ⚠ Needs repair | Hotfix or quick test |

---

## 🧠 Updated Contribution Scenarios

| Scenario                     | Flow                          | Owner        | Tools                                         | Use Case                              |
|-----------------------------|-------------------------------|--------------|-----------------------------------------------|----------------------------------------|
| ✅ Standard Task Flow        | /start → /complete            | GPT Pod      | `commit_and_log()` inside /tasks/complete     | Full lifecycle contribution            |
| 🔁 Reopen + Re-complete      | /start → /complete again      | GPT or Human | `commit_and_log()`                            | Add missing outputs or revisions       |
| 🪛 Hotfix or Backdoor Patch | Manual file edit              | Human        | GitHub UI or CLI → /audit/validate_changelog  | Unstructured change later reconciled   |
| 🧩 Mid-task Output Add       | Add output during work        | GPT or Human | /tasks/commit_and_log_output                  | Append specific outputs mid-task       |



## ✅ Step 5.4: Validate `changelog.yaml`

### 🎯 Why This Step Matters

Your system is designed for **traceability** — every file change should be linked to a task via:

- `task_id`
- `changelog.yaml` entry
- `reasoning_trace.yaml`
- Outputs listed in `task.yaml`

However, during:
- Debugging or patch testing
- Manual edits or hotfixes
- Direct commits via GitHub UI or CLI

…the changelog may become **stale or incomplete**.

---

### 🔍 What `/audit/validate_changelog` Will Do

| Check | Purpose |
|-------|---------|
| ✅ Every task with `done: true` in `task.yaml` has a matching `changelog.yaml` entry | Ensures closed tasks are audit-traced |
| ✅ All output files in `task.yaml[task_id]["outputs"]` are logged in `changelog.yaml` | Links outputs to task events |
| ⚠️ Warn if a file exists in the repo but not in `changelog.yaml` | Detects drift or untracked changes |
| 🔄 Optionally offer to generate missing entries | Restore audit trail automatically |

---

### 🔒 Why This Is Useful

- Detects **repo-task drift**
- Restores **trust** in the system after ad hoc changes
- Enables future **automated audits, patch bundles, and release tracking**
