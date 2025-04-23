# 🚀 Kickoff: AI-Native Patch Engine + Task Runner

This document outlines the next sprint in our AI-native delivery system. Focus: automate patch promotion, streamline task execution, and log traceable delivery metrics.

---

## 🎯 Mission
Build the final execution layer for our AI-native SDLC:
- Pods can run tasks using `task.yaml` + `memory.yaml`
- Outputs are committed via `generate_patch.py`
- Patches are applied via `apply_patch.py`
- Logs, metrics, and task status are auto-updated

---

## 🧩 Key Components

### 1. `generate_patch.py`
- Reads staged changes
- Saves `.patches/patch_<timestamp>_<task_id>.diff`
- Logs:
  - Task ID
  - Files changed
  - Pod
  - Timestamp
  - Patch summary (top-level diff stats)

### 2. `apply_patch.py`
- Copies file outputs from `.patches/` to working repo
- Applies patch or manual overwrite
- Updates Git branch, commits, and pushes
- Optionally opens PR with task ID and summary

### 3. `log_result.py`
- Appends to:
  - `.logs/trace_log.md`
  - `metrics/metrics.yaml`
  - `.logs/feedback/<task_id>.md`
- Updates task.yaml:
  - `status: done`
  - `updated_at`

### 4. `run_task.py`
- Loads task.yaml, memory.yaml, and prompt template
- Optionally uses live GitHub tool for memory
- Passes prompt to GPT or shell AI tool
- Saves outputs to `docs/`, `src/`, `test/`, `.logs/`
- Triggers patch + log workflow

### 5. `next_task.py`
- Lists all `task.yaml` entries with `status: ready`
- Returns the next task, sorted by:
  - Phase
  - Created_at
  - Manual priority flag (optional)

---

## 🛠️ Next Steps
1. [ ] Implement `generate_patch.py`
2. [ ] Implement `apply_patch.py`
3. [ ] Add task/log update utilities
4. [ ] Build test harness for `run_task.py`
5. [ ] Validate with 1 task end-to-end

---

## 📁 File Structure
```
/patch_engine/
  ├── generate_patch.py
  ├── apply_patch.py
  ├── run_task.py
  ├── next_task.py
  └── log_result.py
```

---

## 🧠 Memory
- Tasks live in `task_templates/`
- Memory lives in `memory/`
- Prompts in `prompts/`
- Outputs in `docs/`, `src/`, `tests/`, `.patches/`, `.logs/`

Let’s ship a reusable patch engine and complete our AI-native loop 🚀

