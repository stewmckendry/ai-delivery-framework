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

