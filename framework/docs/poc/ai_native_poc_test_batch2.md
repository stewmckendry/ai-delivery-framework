# 🔥 E2E Test Plan for Discovery Phase (NHL Predictor)

---

## 🎯 Objective

Manually validate the end-to-end (E2E) flow for a Discovery Phase task:

- Task activation
- Prompt retrieval
- Pod task start
- Chain of Thought generation
- Task completion
- Reasoning trace and Git commit

---

## 1. Pre-checks

✅ Confirm FastAPI server is running (Railway + `/openapi.json` access OK)  
✅ Confirm Custom GPT (DeliveryPod) has loaded refreshed schema

---

## 2. Task Activation (DeliveryPod)

**Action**:  
Call `/tasks/activate`

**Payload Example**:
```json
{
  "task_id": "1.1_capture_project_goals",
  "repo_name": "nhl-predictor"
}
```

**Expected Result**:
- Status: 200 OK
- Response contains:
  - `prompt_content`
  - `inputs` (empty or list)
- Git: `task.yaml` shows `status: planned`

---

## 3. Task Start (DevPod/ResearchPod)

**Action**:  
Call `/tasks/start`

**Payload Example**:
```json
{
  "task_id": "1.1_capture_project_goals",
  "repo_name": "nhl-predictor"
}
```

**Expected Result**:
- Status: 200 OK
- Response contains:
  - `prompt_content`
  - `inputs`
- Git:
  - `task.yaml` shows `status: in_progress`
  - `/project/outputs/1.1_capture_project_goals/chain_of_thought.yaml` created

---

## 4. Chain of Thought Generation (Pod Thinking)

**Action**:  
Simulate adding steps manually to `chain_of_thought.yaml` (or auto-via GPT in future batches)

**Example Content**:
```yaml
thoughts:
  - "Analyzed NHL playoff structure"
  - "Selected key factors (goaltending, injuries, etc.)"
  - "Drafted initial prompt to capture project goals"
```

---

## 5. Task Completion

**Action**:  
Call `/tasks/complete`

**Payload Example**:
```json
{
  "task_id": "1.1_capture_project_goals",
  "repo_name": "nhl-predictor"
}
```

**Expected Result**:
- Status: 200 OK
- `reasoning_trace.md` created at:
  ```
  /project/outputs/1.1_capture_project_goals/reasoning_trace.md
  ```
- `task.yaml` updated:
  - `status = completed`
- Auto-commit happens!

---

## 6. Git Verification

**Check `nhl-predictor` repo**:
- New/updated files:
  - `chain_of_thought.yaml`
  - `reasoning_trace.md`
- `task.yaml` reflects correct statuses
- Validate commit messages are sensible (e.g., "Complete task 1.1_capture_project_goals")

---

## ✅ Pass Criteria

- All steps complete without errors
- Artifacts appear in GitHub as expected
- Reasoning trace matches template format
- Tasks move through `planned → in_progress → completed` correctly

---

# 📈 Structured Summary of Current Progress

---

## 🛠 Test Results

| Step | Test Result | Notes |
| :--- | :--- | :--- |
| 1. Activate Task | ✅ | Fixed after updating `project/task.yaml` path |
| 2. Start Task | ✅ | Fixed after correcting prompt file extension |
| 3. Append Chain of Thought | ✅ PASS | Saved cleanly to `/outputs/{task_id}/chain_of_thought.yaml` |

---

# 📋 New Items to Add to the Backlog (Based on Findings)

| ID | New Enhancement | Batch Target |
| :--- | :--- | :--- |
| B6.8 | If prompt file not found during `start_task`, auto-generate a minimal starter prompt | Batch 6 - Hardening |
| B6.9 | Validate prompt paths during project initialization and raise warnings | Batch 6 - Hardening |
| B6.10 | (Optional Stretch) Smart fallback to default templates if missing | Batch 6 - Stretch Goal |

---

# 🚀 Summary

✅ You are already running a **real-world AI-native SDLC cycle** — **very impressive!**  
✅ Clean activation, startup, chain of thought saving flow is now operational.  
✅ Just a few hardening polish steps queued for Batch 6!

---

# ✅ E2E Test Summary – Discovery Phase

| Step | Description | Result |
| :--- | :--- | :--- |
| 1 | Task Activation via `/tasks/activate` | ✅ Success (fixed path to `project/task.yaml`) |
| 2 | Task Start via `/tasks/start` | ✅ Success (after prompt path fix) |
| 3 | Chain of Thought via `/tasks/append_chain_of_thought` | ✅ Success — YAML written to outputs |
| 4 | Reasoning Trace via `/tasks/complete` | ✅ Success (schema bug fixed) |
| 5 | Git Verification | ✅ Success (chain_of_thought, reasoning_trace, `task.yaml` updated) |

# 🔍 Open Issues & Resolutions

---

## 🧭 Prompt Path Issues

**Problem**:  
- `prompt` paths in `task.yaml` mismatched actual file locations.

**Fix**:  
- Human manually updated paths to match:
  ```
  /framework/task_templates/{phase}/{task_id}/prompt_template.md
  ```

✅ **Next Step**:  
- Add **auto-generate fallback** for missing prompts in **Batch 3**.

---

## 🛠️ Task Completion Schema Bug

**Problem**:  
- `/tasks/complete` route expected `repo_name` in body and `task_id` in path, leading to schema mismatch.

**Fix**:  
- Consolidated both fields into body schema. ✅ Issue resolved.

---

## 🧾 Auto-commit Traceability

**Problem**:  
- Output files from task execution (e.g., `project_goals.md`) weren’t committed.

**Fix Proposal**:  
- Wire `auto_commit` into `/tasks/complete`, or expose a **manual fallback tool**.

➡️ **See Batch 3 backlog** to implement this systematically.

---

## 📓 Changelog Update

**Status**:  
- Not yet implemented.

**Action**:  
- Add **auto-changelog write** to every commit-capable route/tool (e.g., activate, start, complete).

📌 **Add to Batch 3** scope.

---

# 📦 Updated Backlog – Batches

---

## ✅ Batch 1: Project Initialization – **COMPLETE**

## ✅ Batch 2: Discovery Phase – **COMPLETE**

---

## 🔄 Batch 3: Development Phase – **IN PROGRESS**

| Step | Action |
| :--- | :--- |
| 3.1 | Implement `/tasks/update_metadata/{task_id}` auto-commit |
| 3.2 | Implement `/tasks/clone` auto-commit |
| 3.3 | Enable auto-save of interim deliverables (e.g., designs) |
| 3.4 | Auto-update chain of thought during dev |
| 3.5 | Wire auto-changelog write into tool handlers |
| 3.6 | Add fallback prompt generator |
| 3.7 | Auto-commit generated outputs (e.g., `project_goals.md`) |
| 3.8 | Add `append_reasoning_trace` route if needed |

---

## 🔄 Batch 4: Testing Phase

| Step | Action |
| :--- | :--- |
| 4.1 | Implement `/memory/index` auto-commit |
| 4.2 | Implement `/memory/add` auto-commit |
| 4.3 | Add test capture of E2E readiness in reasoning trace |
| 4.4 | Expand system prompts for test validations |
| 4.5 | Test full traceable workflows |

---

## 🔄 Batch 5: Cutover & Go-Live

| Step | Action |
| :--- | :--- |
| 5.1 | Implement `/tasks/append_handoff_note/{task_id}` |
| 5.2 | Finalize handoff process |
| 5.3 | Formalize `promote_patch` PR bundle |
| 5.4 | Validate `CHANGELOG.md` updates across system |
| 5.5 | Validate memory coherence |
| 5.6 | Publish NHL PoC App and Audit |

---

## 🔄 Batch 6: System Hardening

| Step | Action |
| :--- | :--- |
| 6.1 | Rollback strategy for failed deployments |
| 6.2 | Integrate reasoning metrics |
| 6.3 | Human onboarding guide |
| 6.4 | Multi-pod orchestration |
| 6.5 | Init: capture chain_of_thought |
| 6.6 | Init: link project context in memory |
| 6.7 | Init: enrich `reasoning_trace.md` |
| 6.8 | Init: persist prompt used |
| 6.9 | Init: auto-update changelog |
| 6.10 | GitHub failsafe + retry wrappers |

