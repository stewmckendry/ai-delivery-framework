# AI-Native Delivery System: End-to-End Workflow Guide

> This guide describes the full lifecycle of AI-native delivery using GPT-powered pods, GitHub automation, and traceable handoffs. It is designed to be fully executable today, while also describing how the process will evolve in the future.

---

## Table of Contents
1. [Overview](#overview)
2. [Roles and Responsibilities](#roles-and-responsibilities)
3. [Step-by-Step Delivery Process](#step-by-step-delivery-process)
4. [Technical Implementation](#technical-implementation)
5. [What’s Built vs. What’s Next](#whats-built-vs-whats-next)
6. [Future-State Vision](#future-state-vision)

---

## Overview

This system enables humans and GPT-based "pods" to collaborate on building and shipping features using structured prompts, tracked patches, and automated GitHub pull requests. Each pod (e.g. Dev, QA, Research, Delivery) performs specific work, submits a patch, and hands it off to the next pod. Git is the system of record.

All GPT work is logged, traceable, and reviewable using standardized metadata (`thought_trace.yaml`, `changelog.yaml`, etc.) and GitHub PRs.

---

## Roles and Responsibilities

### Human Lead
- Assigns work to GPT pods using structured prompts
- Reviews output patches and pull requests
- Approves and merges PRs
- Ensures correct pod-to-pod handoffs
- Downloads GPT-generated output files and places them in project folders

### GPT Pod (e.g. Dev, QA, Research)
- Receives task via structured prompt
- Loads context files using reference paths or GitHub links
- Generates a `.diff` patch and supporting logs
- Notifies human to download output from sandbox

---

## Step-by-Step Delivery Process

### 1. Assign Work to a Pod

The human or previous pod prepares the prompt:

```bash
python scripts/assign_task.py --to qa-pod --task F2.1
```

- Uses prompt template from `prompts/qa_pod.txt`
- Injects `input_files`, `instructions`, and `task_id`

**Example Prompt Packet Structure:**
```yaml
pod: qa-pod
task_id: F2.1
goal: Add unit tests for symptom parser
input_files:
  - src/models/agent/concussion_agent.py
instructions: Focus on edge case symptoms and return-to-play stage transitions
```

---

### 2. Pod Does the Work

The GPT pod:
- Loads the input files and context
- Runs the logic or generates the patch
- Produces:
  - `/mnt/data/patch_*.diff`
  - `/mnt/data/thought_trace.yaml`
  - `/mnt/data/changelog.yaml`
  - `/mnt/data/handoff_log.yaml`

GPT then notifies the human:
> "Patch and logs for F2.1 are ready. Please download:
> - patch_20250419_123456.diff
> - thought_trace.yaml
> - changelog.yaml
> - handoff_log.yaml"

---

### 3. Human Saves Files to Local Repository

The human downloads the files using the ChatGPT UI and saves them to the appropriate project folders:

- `.patches/queue/patch_*.diff`
- `.logs/thought_trace.yaml`
- `.logs/changelog.yaml`
- `.logs/handoff_log.yaml`

Optionally use a helper script (e.g. `download_patch_from_chatgpt.py`) to automate file moves from `Downloads/` to project structure.

---

### 4. Promote Patch to GitHub

Run the promotion script:
```bash
python scripts/patch_promoter.py
```

This script:
- Moves `.diff` from `.patches/queue/` to `.patches/`
- Stages supporting logs (`.logs/*.yaml`)
- Runs `git add`, `git commit`, `git push`
- Pushes to `main` branch

---

### 5. GitHub App + Action Trigger

Once pushed:
- The `AI Patch Promoter` GitHub App receives the webhook event
- The app clones the repo, detects `.diff`, applies it, and opens a PR

OR

- A GitHub Action like `apply_patch_enhanced.yaml` is triggered
- It reads the `.diff`, applies it, and opens a PR with:
  - Thought trace log
  - Changelog
  - Handoff metadata

> Note: GitHub App and GitHub Action serve similar roles. Use one to avoid duplication.

---

### 6. Review & Approve PR

Human lead:
- Opens the PR auto-created by GitHub
- Reviews code diff, logs, and reasoning
- Comments if changes needed
- Approves and merges when ready

---

### 7. Handoff to Next Pod

The GPT pod or human includes the next pod in `handoff_log.yaml`:

```yaml
from: qa-pod
to: delivery-pod
reason: Feature is tested and ready for release
related_patch: patch_20250419_123456.diff
```

The next pod is assigned by:
- Reviewing PR labels
- Or using a script like:
```bash
python scripts/assign_task.py --from handoff_log.yaml
```

---

## Technical Implementation

### Code and Scripts
- `generate_patch.py`: GPT patch + log generation
- `patch_promoter.py`: Moves files from `.patches/queue/` to `.patches/`, stages, and commits
- `create_pr_from_patch.sh`: Applies `.diff` and opens PR (used in some cases)
- `assign_task.py`: Builds structured pod prompt + file context for next pod
- `download_patch_from_chatgpt.py` (planned): Moves downloaded patch/logs to project structure

### GitHub Integration
- **GitHub App**: `AI Patch Promoter`
  - Webhook on `push`
  - Applies `.diff`, opens PR
- **GitHub Action**: `apply_patch_enhanced.yaml`
  - Validates `.diff`
  - Opens PR with logs and tags

### Folder Layout
```
.patches/
├── queue/                # Pod output awaiting promotion
├── patch_*.diff          # Git-ready patches

.logs/
├── changelog.yaml
├── handoff_log.yaml
├── thought_trace.yaml
```

### Prompts
```
prompts/
├── dev_pod.txt
├── qa_pod.txt
├── delivery_pod.txt
```

---

## What’s Built vs. What’s Next

### ✅ Built So Far
- GPT → `.diff` + logs in sandbox
- GitHub App (PR promotion)
- Logging and trace metadata
- Prompt template convention

### 🔧 To Build Next
- `patch_promoter.py`: automate queue-to-patch flow
- `assign_task.py`: structured pod prompt generation
- `download_patch_from_chatgpt.py`: move downloaded files to local repo
- Handoff loop between pods
- Slack or webhook triggers for promoting patches

---

## Future-State Vision

### Improvements Coming Soon
- GPT writes directly to GitHub (via CLI/API)
- PRs include AI-generated changelog and reviewers
- Pods pull latest code via GitHub API
- Logs auto-populate metrics dashboard
- Pod queue watches for triggers via cron or webhook

### Fully Autonomous Workflow
1. Dev Pod submits `.diff` + logs → auto-pushed
2. GitHub App applies, opens PR
3. QA Pod reviews, submits tests
4. Delivery Pod packages release

---

## Summary

You now have a reproducible, AI-native delivery model. With GPT doing the work, GitHub managing code, and humans reviewing outcomes, you’re ready to scale feature delivery — one autonomous patch at a time.
