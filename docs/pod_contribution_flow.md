# 🚀 Onboarding Snippet: AI-Native Pod Patch Contribution Flow

Welcome to the AI-Native Delivery System! This guide outlines how Pod contributors (powered by GPT) can submit output files into GitHub using metadata-driven patches — ensuring traceability, automation, and a smooth human-in-the-loop workflow.

---

## 🎯 Purpose
Enable any Pod (DevPod, QAPod, etc.) to:
- Finalize structured output files with a human collaborator
- Zip and submit files + metadata as one deliverable
- Trigger patch generation, branch creation, and PR

---

## ♻️ Contribution Flow

### ✅ Step 1: Finalize Output in Chat
- Human and Pod complete the assigned task together
- Pod confirms all output files are finalized and ready to promote

### ✅ Step 2: GPT Shares Output ZIP + Metadata
- Pod zips all output files (preserving repo-relative paths)
- Includes a `metadata.json` inside the ZIP:

```json
{
  "task_id": "2.3_build_feature_prompting",
  "summary": "Implements logic to select and trigger custom prompts.",
  "output_files": [
    "docs/features/prompting_logic.md",
    "prompts/dev/feature_prompt.txt"
  ]
}
```

- GPT returns a **download link** to the ZIP

### ✅ Step 3: Human Promotes the Patch
- Download the ZIP
- Save it to `chatgpt_repo/outputs/`
- Run:

```bash
bash scripts/generate_patch_from_output.sh
```

This script:
- Extracts metadata from the ZIP
- Stages files using metadata paths
- Looks up `task_id` in the central `task.yaml` backlog
- Derives `branch_name` using `task.yaml.tasks[task_id].category`
- Creates `.diff`, `.json`, and calls `create_pr_from_patch.sh`

### ✅ Step 4: PR is Created and Reviewed
- Script pushes the branch and opens a GitHub PR
- Human reviews, optionally edits, and merges it

---

## 🧠 How Branch Naming Works

```bash
chatgpt/auto/<category>/<task_id>
```

Examples:
- `chatgpt/auto/dev/2.3_build_feature_prompting`
- `chatgpt/auto/qa/2.3_build_feature_prompting`
- `chatgpt/auto/cutover/4.1_launch_checklist`

> `category` is pulled from a centralized `task.yaml` file, which stores metadata for all tasks in the project. The script extracts `task_id` from `metadata.json` and uses it to locate the correct entry under `tasks:`.

---

## 🧰 Supporting Scripts

### `generate_patch_from_output.sh`
- Reads `task.yaml` and metadata
- Stages files, sets branch name, creates diff

### `create_pr_from_patch.sh`
- Reads `.json` metadata
- Applies patch, commits, pushes, opens PR

### `prune_old_branches.sh`
- Prunes merged `chatgpt/auto/*` branches

---

## 📂 Directory Layout

| Folder                  | Purpose                         |
|-------------------------|----------------------------------|
| `chatgpt_repo/outputs/` | ZIP files from GPT               |
| `.patches/`              | Git patch diffs                  |
| `.logs/patches/`         | JSON metadata for each patch     |
| `task.yaml`              | Full project backlog of all tasks|

---

## 🤝 Responsibilities

| Actor         | Responsibilities                                                  |
|---------------|-------------------------------------------------------------------|
| **GPT Pod**   | Finalize outputs + metadata, return ZIP for download              |
| **Human**     | Download files, run promotion script, review PR                   |
| **Script**    | Generate patch, update metadata, set branch, automate PR process  |

---

## 🧪 Example Live Task
- **Task:** 2.3_build_feature_prompting
- **Pod:** DevPod GPT
- **Output:** `prompting_logic.md`, `feature_prompt.txt`
- **Branch:** `chatgpt/auto/dev/2.3_build_feature_prompting`
- **Patch Metadata:** `.logs/patches/patch_20250424_XXXX_2.3_build_feature_prompting.json`
- **PR:** Opened and reviewed

---

Let’s keep shipping clean, structured patches from AI-native Pods 🚀

