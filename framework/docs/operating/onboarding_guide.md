# 🧭 Human Lead Onboarding Guide

Welcome to the AI-Native Delivery System! This guide is your reference for how the system works, how to run tasks, and how to guide GPT Pods through structured, traceable delivery.

---

## 📌 1. System Overview

This system enables AI-assisted, task-based software delivery using:

- **YAML-based memory and task tracking**
- **Structured reasoning capture (`reasoning_trace.yaml`)**
- **OpenAPI-driven GPT tooling**
- **Git versioning + changelog auditing**
- **Pod workflows (DevPod, QAPod, ProductPod, etc.)**

---

## 📁 2. Repo Structure

| Folder | Purpose |
|--------|---------|
| `project/task.yaml` | Prescribes all tasks: inputs, owners, status |
| `project/memory.yaml` | Tracks meaningful files + metadata |
| `project/outputs/<task_id>/` | Logs for each task (chain of thought, outputs, reasoning) |
| `project/.logs/` | Changelogs and rollback logs |
| `project/docs/` | System and onboarding documentation |

---

## 🔄 3. Task Lifecycle

| Phase | Tool | Description |
|-------|------|-------------|
| Start Task | `/tasks/start` | Marks task in progress, returns prompt, inputs, handoff |
| Log Thoughts | `/tasks/append_chain_of_thought` | Appends structured reasoning |
| Complete Task | `/tasks/complete` | Submits outputs, reasoning trace, handoff note |
| Reopen Task | `/tasks/reopen` | Reopens task and logs reasoning why |

Each task has a reasoning trace saved in:  
`project/outputs/<task_id>/reasoning_trace.yaml`

---

## ⚙️ 4. Key GPT Tools

| Tool | Use |
|------|-----|
| `/tasks/update_metadata` | Update fields like description, inputs, outputs |
| `/tasks/activate` | Mark multiple tasks as ready or in-progress |
| `/tasks/clone` | Clone an existing task |
| `/tasks/create` | Create a brand new task |
| `/tasks/getTaskDetails` | Retrieve task metadata |
| `/tasks/next` | Get next recommended task |
| `/memory/index` | Index files in memory.yaml |
| `/memory/search` | Search memory for relevant files |
| `/memory/diff` | Detect missing memory entries |
| `/memory/validate-files` | Confirm files exist in GitHub + memory |
| `/tasks/commit_and_log_output` | Mid-task file commit with changelog |
| `/audit/validate_changelog` | Backfill missing changelog entries |
| `/git/rollback_commit` | Revert files from prior commit |
| `/getFile` and `/batch-files` | Retrieve file contents from GitHub |
| `/actions/list` | List all tools by category with descriptions |

---

## 📊 5. Logs & Reports

| Report | File |
|--------|------|
| Changelog | `project/outputs/changelog.yaml` |
| Reasoning Trace | `project/outputs/<task_id>/reasoning_trace.yaml` |
| Metrics Report | `project/outputs/reports/metrics_report_<timestamp>.yaml` |
| Reverts | `project/.logs/reverted_commits.yaml` |

---

## 🛑 6. Rollback a Commit

Use `/git/rollback_commit` and pass:

{
  "repo_name": "your-repo",
  "commit_sha": "<sha>",
  "paths": ["project/task.yaml"],
  "reason": "Undo accidental memory index"
}

Commit SHAs can be found via:
- GitHub web → Commits tab
- `git log` in terminal
- changelog or rollback logs

---

## 💡 7. Tips & Examples

- You can start any task by calling `/tasks/start` and following the `next_step`.
- GPT will suggest tools, but you can guide it to use `/memory/search`, `/tasks/complete`, or `/metrics/summary`.
- Logs are automatically committed — use `/git/rollback_commit` to fix mistakes.

---

## ✅ You're Ready!

Welcome aboard. You're now set up to lead an AI-native delivery project — repeatable, traceable, and faster than ever.
