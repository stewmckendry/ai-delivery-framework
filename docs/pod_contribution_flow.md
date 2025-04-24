# 🧩 AI-Native Delivery: Pod Patch Contribution Flow

This document outlines the standardized process for ChatGPT Pods to contribute work into the shared GitHub repository using output files and metadata, ensuring human-in-the-loop review, traceability, and automation-friendly tooling.

---

## 🌟 Purpose
Enable any Pod to:
- Finalize one or more output files collaboratively with a human
- Generate a patch from the new files
- Attach metadata for automation and traceability
- Let the human apply, push, and open a PR for review

---

## ♻️ Contribution Flow

### Step 1: Finalize Output in Chat
- Human + Pod iterate on a task until all output files are finalized
- Human prompts GPT to share final outputs and metadata

### Step 2: GPT Shares Output Files & Metadata
- GPT zips and returns download link for finalized files
- GPT generates and returns a metadata JSON:
  ```json
  {
    "task_id": "1.1_capture_project_goals",
    "summary": "Capture and describe project goals",
    "output_folders": ["docs"]
  }
  ```
- Human downloads:
  - Finalized output files → saved to `chatgpt_repo/outputs`
  - Metadata JSON → saved to `.logs/patches/`

### Step 3: Promote Patch via Script
- Human runs `scripts/generate_patch_from_output.sh`
- This script:
  - Loads latest metadata from `.logs/patches/`
  - Moves files from `chatgpt_repo/outputs/` into correct folders
  - Generates `.diff` file from `git diff --staged`
  - Writes updated `.json` metadata in `.logs/patches/`
  - Calls `create_pr_from_patch.sh`

### Step 4: PR Review
- Script creates a branch, pushes, and opens a pull request
- Human reviews and merges the PR into `main`

---

## 🛠️ Supporting Scripts and Tools

### ✅ `generate_patch_from_output.sh`
- Uses `.logs/patches/*.json` metadata to locate files
- Applies staged changes, creates `.diff`, and calls PR script

### ✅ `create_pr_from_patch.sh`
- Applies patch to new branch, commits, pushes, opens PR

---

## 🧠 Prompt Template: `promote_output_files.txt`
```txt
---
tool: output_file_promotion
---

🎯 FINALIZE OUTPUT FILES

You have completed your work on this task.

Please:
1. Upload and return **downloadable links** for finalized output files (as a zipped folder)
2. Generate and return **metadata JSON** with the following format:

```json
{
  "task_id": "1.1_capture_project_goals",
  "summary": "Capture and describe project goals",
  "output_folders": ["docs"]
}
```

3. Print a summary with:
- Instructions for the human to download and unzip the output files
- Instructions to store metadata in `.logs/patches/`
- CLI to run: `bash scripts/generate_patch_from_output.sh`
```

---

## 📁 Directory Conventions

| Folder | Purpose |
|--------|---------|
| `chatgpt_repo/outputs/` | Temporary folder for GPT-generated outputs |
| `.patches/` | Final promoted patch files |
| `.logs/patches/` | Metadata for each patch task |
| `.logs/trace_log.md` | Trace of patches and contributors |

---

## 📌 Custom GPT Action: `output_file_promotion`

| Purpose | Returns download links for finalized files and metadata |
|---------|----------------------------------------------------------------|

**Returns:**
- `output_files.zip` download URL
- `metadata.json` download URL

---

## ✅ Live Test Result: MemoryPod End-to-End
- **Pod:** MemoryPod GPT
- **Task:** 1.1_capture_project_goals
- **Success:** Output finalized, metadata returned, patch created, PR opened
- **Download Metadata:** `.logs/patches/patch_20250423_205405_1.1_capture_project_goals.json`
- **Pull Request:** [PR #16](https://github.com/stewmckendry/ai-concussion-agent/pull/16)

---

## 🤖 Responsibilities Summary

| Actor | Responsibilities |
|-------|------------------|
| **ChatGPT Pod** | Finalize output files, return zipped output + metadata JSON |
| **Human** | Download files, place in repo folders, run patch script, review PR |
| **Script** | Automates patch creation, metadata logging, PR creation |

Let’s use this modernized output-based process to streamline Pod contributions and eliminate diff errors for good 🚀

