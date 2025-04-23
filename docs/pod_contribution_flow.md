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
  - Simulates running `generate_patch.py` in the sandbox
  - Collects staged file changes and constructs a `.diff`
  - Outputs metadata:
    ```json
    {
      "patch_file": ".patches/patch_20250422_103045_2.3_build_metrics_tool.diff",
      "task_id": "2.3_build_metrics_tool",
      "summary": "Added metrics tracker logic",
      "output_folders": ["docs/", "metrics/"]
    }
    ```
  - Returns the `.diff` file and metadata to the human for download

> ⚠️ **Note:** Since ChatGPT cannot access or clone the repo directly, it determines file destinations using the `outputs` field in `task.yaml`. These serve as hints about where the human should place the generated content, and help structure metadata for patch creation.

### Step 3: Human Downloads Patch File
- Human (or GPT) uses a `GET /patches/{patch_name}` endpoint to retrieve the patch content
- Patch is saved locally into `chatgpt_repo/.patches/`

### Step 4: Promote Patch via Script
- Human runs `scripts/promote_patch.sh` which:
  - Moves the patch from `chatgpt_repo/.patches/` into `.patches/`
  - Calls `create_pr_from_patch.sh` with the patch name
  - Applies the patch, creates a feature branch, and pushes to GitHub
  - Opens a pull request (PR) using `gh` CLI if available

### Step 5: PR Review
- Human reviews and approves the PR
- PR is merged into `main`
- Optional GitHub Action (`promote_patch.yaml`) auto-runs on new `.patches/*.diff` files to trigger PR creation (if `promote_patch.sh` wasn't used)

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
- Automatically runs `create_pr_from_patch.sh` for hands-off promotion

### ✅ `GET /patches/{patch_name}` (FastAPI route)
- Returns the raw `.diff` file content for download
- Allows human or GPT to fetch the patch after promotion step

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
- Simulates running `generate_patch.py` inside the GPT sandbox
- Returns metadata needed for patch promotion and review

**Input Parameters:**
```json
{
  "task_id": "string",
  "output_folders": ["string"],
  "summary": "string"
}
```

**Returns:**
```json
{
  "patch_file": "string",
  "task_id": "string",
  "summary": "string",
  "output_folders": ["string"]
}
```

Used as the final step in the Pod output generation to signal a human to run local promotion. The `output_folders` are derived from `task.yaml.outputs` and serve as guidance.

---

## 🤖 Responsibilities Summary

| Actor | Responsibilities |
|-------|------------------|
| **ChatGPT Pod** | Generate output files, call `promote_patch` GPT action, return `.diff` + metadata to human |
| **Human** | Fetch patch from `/patches/{name}`, save locally, run `promote_patch.sh`, approve PR |
| **GitHub Action** | (Optional) Auto-promote any `.diff` committed to `.patches/` by running `create_pr_from_patch.sh` |

---

Let’s use this standardized process to keep our delivery loop fast, safe, and trackable across all Pods 🚀

