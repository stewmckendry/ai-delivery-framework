# 🧪 Batch 3 Test Script: `nhl-predictor`

---

## 🎯 Goal

Simulate an **end-to-end test** of the Discovery and Development phases for the `nhl-predictor` PoC using the newly implemented AI-Delivery-Framework routes.

---

## ✅ Pre-Test Instructions

In the `nhl-predictor` repo:

1. **Delete** (if exists):
   ```
   /project/outputs/1.1_capture_project_goals/reasoning_trace.yaml  
   /project/outputs/changelog.yaml
   ```

2. **Update** `/project/task.yaml`:

   - For task `1.1_capture_project_goals`:
     ```yaml
     status: planned
     done: false
     ```

---

## 🧪 Test Sequence

### 🔹 Step 1: Resume Task 1.1
```http
POST /tasks/start
{
  "task_id": "1.1_capture_project_goals",
  "repo_name": "nhl-predictor"
}
```
✅ **Expect**: Prompt and inputs returned

---

### 🔹 Step 2: Append Thought
```http
POST /tasks/append_chain_of_thought
{
  "task_id": "1.1_capture_project_goals",
  "repo_name": "nhl-predictor",
  "message": "Iterating on goals summary"
}
```

---

### 🔹 Step 3: Complete Task 1.1
```http
POST /tasks/complete
{
  "task_id": "1.1_capture_project_goals",
  "repo_name": "nhl-predictor",
  "outputs": [
    {
      "path": "docs/project_goals.md",
      "type": "markdown",
      "content": "# Project Goals\n\nBuild a fun AI-powered app to predict NHL outcomes while proving our AI Delivery Framework."
    }
  ]
}
```

---

### 🔹 Step 4: Repeat for Remaining Discovery Tasks

**Tasks**:
- `1.2_define_user_flows`
- `1.3_decompose_features`
- `1.4_write_acceptance_criteria`
- `1.6_define_architecture`

**For each task**:
1. `POST /tasks/activate`
2. `POST /tasks/start`
3. `POST /tasks/append_chain_of_thought` — simple message
4. `POST /tasks/complete` — simple markdown output (e.g., `docs/*.md`)

---

### 🔹 Step 5: Repeat for Development Tasks

**Tasks**:
- `2.1_design_feature`
- `2.2_build_feature`
- `2.3_QA_feature`
- `2.4a_fix_bugs`
- `2.4b_retest_fixes`
- `2.7_prep_deploy_guide`

Same sequence:
- Activate ➝ Start ➝ Append Thought ➝ Complete with short output

📝 Keep content lightweight: 1–2 sentence markdown + minimal thoughts

---

## ✅ Test Completion Criteria

- All Discovery + Dev tasks show:  
  ```yaml
  status: completed
  ```

- Each task has:
  - `chain_of_thought.yaml`
  - `reasoning_trace.yaml`
  - Entry in `/changelog.yaml`
  - At least **1 output file** in `docs/` or `project/outputs/`

