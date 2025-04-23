# 🧩 AI-Native Delivery: Pod Patch Contribution Flow

This document outlines the standardized process for ChatGPT Pods to contribute work into the shared GitHub repository using patches, ensuring human-in-the-loop review, traceability, and automation-friendly tooling.

---

## 🌟 Purpose
Enable any Pod to:
- Finalize an output collaboratively with a human
- Generate a patch representing the change
- Attach metadata for automation and traceability
- Let the human apply, push, and open a PR for review

---

## ♻️ Contribution Flow

### Step 1: Finalize Output in Chat
- Human + Pod iterate on an output file (e.g., markdown, Python, YAML)
- When final, the human signals the Pod to generate a patch

### Step 2: Generate Patch via Custom GPT Action
- Pod calls the `promote_patch` **custom GPT action**, which:
  - Accepts `task_id`, `summary`, `output_folders`, and the full `diff` string
  - Saves the `.diff` file to `/mnt/data/.patches/` on the FastAPI backend
  - Returns metadata and a **`download_url`**:
    ```json
    {
      "patch_file": "patch_1.1_capture_project_goals.diff",
      "task_id": "1.1_capture_project_goals",
      "summary": "Refined project goals and improved formatting",
      "output_folders": ["docs"],
      "download_url": "https://ai-concussion-agent-production.up.railway.app/patches/patch_1.1_capture_project_goals.diff"
    }
    ```
  - The human clicks the `download_url` to save the patch into `chatgpt_repo/.patches/`

> ⚠️ **Note:** GPT generates the unified diff. For new files, it uses `--- /dev/null` as the original file. For modified files, it compares against the fetched original.

### Step 3: Promote Patch via Script
- Human saves the downloaded `.diff` file into `chatgpt_repo/.patches/`
- Runs `scripts/promote_patch.sh` which:
  - Moves the patch from `chatgpt_repo/.patches/` into `.patches/`
  - Calls `create_pr_from_patch.sh` with the patch name
  - Applies the patch, creates a feature branch, and pushes to GitHub
  - Opens a pull request (PR) using `gh` CLI if available

### Step 4: PR Review
- Human reviews and approves the PR
- PR is merged into `main`

> 💡 **Fallback automation:** A GitHub Action (`promote_patch.yaml`) watches `.patches/*.diff` and auto-runs `create_pr_from_patch.sh` if the patch was committed but not manually promoted. This ensures patches are never left idle. Use this as a backup or for CI-based workflows.

---

## 🛠️ Supporting Scripts and Tools

### ✅ `generate_patch.py`
- Local CLI script for creating a `.diff` file from staged changes
- Used as reference for the logic behind the `promote_patch` custom GPT action
- Inputs: task ID, optional output folders, summary
- Output: `.patches/*.diff` and `.logs/patches/*.json`

### ✅ `create_pr_from_patch.sh`
- Applies the patch to a new Git branch
- Commits, pushes, and opens a PR
- Accepts `TRIGGERED_PATCH` env var for GitHub Action compatibility

### ✅ `promote_patch.sh` (human-run wrapper)
- Moves patch from `chatgpt_repo/.patches/` to `.patches/`
- Sets `TRIGGERED_PATCH` and calls `create_pr_from_patch.sh`

### ✅ `.github/workflows/promote_patch.yaml`
- GitHub Action that detects `.patches/*.diff` added to repo
- Automatically runs `create_pr_from_patch.sh`
- **Note:** This is a fallback for patches committed manually or via automation. The preferred method is running `promote_patch.sh` locally.

---

## 🧠 Prompt Templates

### `promote_patch_existing_file.txt`
```txt
---
tool: promote_patch
task_id: 1.1_capture_project_goals
output_folders: ["docs"]
use_case: existing_file
input_file: docs/project_goals.md
summary: Refined project goals and improved formatting
---

🎯 PROMOTE PATCH – EXISTING FILE

You have finalized the updated version of the file: `docs/project_goals.md`.

Please:
1. Compare your updated version to the original version (fetched using `getGitHubFile`)
2. Generate a unified diff in standard Git format
3. Call the `promote_patch` tool with the patch metadata and diff.
```

### `promote_patch_new_file.txt`
```txt
---
tool: promote_patch
task_id: 2.5_document_return_to_play
output_folders: ["docs"]
use_case: new_file
new_file: docs/return_to_play.md
summary: Added initial return-to-play protocol document
---

🆕 PROMOTE PATCH – NEW FILE

You have created a new file as part of your task output: `docs/return_to_play.md`.

Please:
1. Format a unified diff that represents adding this new file
2. Use the correct Git-style diff structure:
   - `--- /dev/null`
   - `+++ b/docs/return_to_play.md`
   - Followed by `+` for each line of content
3. Call the `promote_patch` tool with:
   - task_id
   - summary
   - output_folders
   - diff
```

---

## 📁 Directory Conventions

| Folder | Purpose |
|--------|---------|
| `.patches/` | Stores committed patches to be applied and promoted to PRs |
| `chatgpt_repo/.patches/` | Temporary folder for downloaded GPT-generated patches |
| `.logs/patches/` | Metadata for each patch (task ID, summary, output folders) |
| `.logs/trace_log.md` | Chronological log of applied patches |
| `metrics/metrics.yaml` | Tracks delivery metrics per patch/task |

---

## 📌 Custom GPT Action: `promote_patch`

A tool that can be called by a ChatGPT Pod when a task output is finalized. It:
- Accepts metadata and real unified diff string
- Saves the `.diff` to server disk
- Returns a `download_url` for the human to fetch and promote

**Input Parameters:**
```json
{
  "task_id": "string",
  "summary": "string",
  "output_folders": ["string"],
  "diff": "string"
}
```

**Returns:**
```json
{
  "patch_file": "string",
  "task_id": "string",
  "summary": "string",
  "output_folders": ["string"],
  "download_url": "string"
}
```

---

## ✅ Live Test Result: MemoryPod End-to-End
- **Pod:** MemoryPod GPT
- **Task:** 1.1_capture_project_goals
- **Success:** Fetched input → iterated with human → generated diff → promoted patch → returned download link
- **Download URL:** [patch_1.1_capture_project_goals.diff](https://ai-concussion-agent-production.up.railway.app/patches/patch_1.1_capture_project_goals.diff)
- **Summary File:** `poc_test_results_e2e_1.md`

---

## 🤖 Responsibilities Summary

| Actor | Responsibilities |
|-------|------------------|
| **ChatGPT Pod** | Generate output files, call `promote_patch`, return patch file + metadata + download URL |
| **Human** | Download `.diff` file, run `promote_patch.sh`, approve PR |
| **GitHub Action** | Auto-promotes committed `.diff` files if human script isn't used — serves as fallback for unattended patch workflows |

---

Let’s use this standardized process to keep our delivery loop fast, safe, and trackable across all Pods 🚀

