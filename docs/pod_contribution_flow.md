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
- Includes the following in the ZIP:
  - `metadata.json`
  - `reasoning_trace.md`
  - `prompt_used.txt`

#### 📄 Example `metadata.json`:
```json
{
  "task_id": "2.3_build_feature_prompting",
  "summary": "Implements logic to select and trigger custom prompts.",
  "output_files": [
    "docs/features/prompting_logic.md",
    "prompts/dev/feature_prompt.txt"
  ],
  "prompt": "prompts/used/DevPod/2.3_build_feature_prompting_prompt.txt"
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
- Extracts metadata, prompt, and reasoning
- Stages files using metadata paths
- Updates `task.yaml`, changelog, reasoning logs
- Opens a PR with a detailed markdown body

### ✅ Step 4: PR is Created and Reviewed
- Script pushes the branch and opens a GitHub PR
- Human reviews, optionally edits, and merges it

---

## 🧠 Prompt Tracking Mission & Flow

To ensure transparency and repeatability, we track the actual prompt used for each task. This prompt:
- Is saved in `prompt_used.txt`
- Is included in the ZIP and stored under `prompts/used/<assigned_pod>/<task_id>_prompt.txt`
- Is quoted in the pull request body

Prompts are either fetched using `getGitHubFile`, or provided manually by the human if the tool fails.

---

## 🧰 Supporting Scripts

### `generate_patch_from_output.sh`
- Reads `task.yaml`, `metadata.json`, `prompt_used.txt`, and `reasoning_trace.md`
- Stages files, sets branch name, creates diff
- Updates `.logs/` and `prompts/used/` directories

### `create_pr_from_patch.sh`
- Reads `.json` metadata
- Applies patch, commits, pushes, opens PR
- Injects human-friendly PR body from changelog, reasoning, and prompt

### `prune_old_branches.sh`
- Prunes merged `chatgpt/auto/*` branches

---

## 📂 Directory Layout

| Folder                    | Purpose                                  |
|---------------------------|-------------------------------------------|
| `chatgpt_repo/outputs/`   | ZIP files from GPT                        |
| `.patches/`               | Git patch diffs                           |
| `.logs/patches/`          | JSON metadata for each patch              |
| `.logs/changelogs/`       | Markdown changelogs per task              |
| `.logs/reasoning/`        | Reasoning summaries per task              |
| `prompts/used/<pod>/`     | Actual prompt used for each Pod+task      |
| `task.yaml`               | Full project backlog of all tasks         |

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
- **Prompt:** `prompts/used/DevPod/2.3_build_feature_prompting_prompt.txt`
- **PR:** Opened and reviewed

---

Let’s keep shipping clean, structured patches from AI-native Pods 🚀

