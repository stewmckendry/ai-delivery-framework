### 2.3 QA Review and Test Feature
```markdown
🎯 POD MISSION: QAPod – QA Review and Test Feature

🧾 TASK YAML:
task_id: 2.3_qa_review_feature  
pod: QAPod  
description: Perform QA review of the implemented feature, validate against spec and acceptance criteria, create and run test cases, and document QA results  
inputs:
  - docs/specs/spec_<feature_id>.md
  - src/feature_<feature_id>/**/*
  - tests/feature_<feature_id>/**/*
  - docs/qa/acceptance_matrix.md

📁 MEMORY:
- path: docs/specs/spec_<feature_id>.md  
  repo: stewmckendry/ai-delivery-framework
- path: docs/qa/acceptance_matrix.md  
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.
---

### ✅ QA Instructions

1. **Create a QA Test Plan**
   - Summarize the scope of testing  
   - Identify types of tests to be performed (e.g., functional, edge cases, LLM response validation, regression)  
   - Define pass/fail criteria and risks

2. **Define Test Cases and Required Data**
   - Write detailed test cases for each acceptance criterion and user flow  
   - Document any mock inputs, API responses, prompts, or data assumptions  
   - Consider failure modes, edge cases, and invalid inputs

3. **Perform Feature QA Review**
   - Validate implementation against the tech spec  
   - Ensure standards are met for logging, traceability, and LLM safety  
   - Check if DevPod’s unit tests sufficiently cover acceptance criteria

4. **Run Functional & Regression Tests**
   - Execute manual and automated test cases  
   - Run regression tests on impacted tools/modules  
   - Log results clearly with screenshots or debug output if needed

5. **Document QA Results**

For each test case, capture:

📋 **QA Result Metadata**
- `test_case_id`: Unique test case identifier  
- `feature_id`: Corresponding feature ID  
- `description`: Brief purpose of the test  
- `steps`: Step-by-step procedure  
- `expected_result`: What should happen  
- `actual_result`: What actually happened  
- `status`: Passed, Failed, Blocked  
- `linked_criteria`: ID(s) of related acceptance criteria  
- `run_by`: QA reviewer name or pod  
- `run_at`: Timestamp of execution

---

### 📥 Save Outputs
- `test/feature_<feature_id>/qa_test_plan.md` — Summary of scope, test types, and risks  
- `test/feature_<feature_id>/qa_test_cases.md` — List of defined test cases with inputs, steps, and expected outcomes  
- `test/feature_<feature_id>/qa_test_results.md` — Results for executed test cases  
- `docs/qa/acceptance_matrix.md` — Update test coverage and validation status

---

📌 Optional Enhancements:
- Add screenshots, logs, or LLM inputs/outputs to `test/feature_<feature_id>/artifacts/`  
- Flag ambiguous acceptance criteria using `> [FOLLOW-UP]` or `> [GAP]` in the spec  
- Coordinate fixes or retests with DevPod when necessary
