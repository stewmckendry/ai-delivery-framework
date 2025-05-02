### 3.2 Prompt Template
```markdown
🎯 POD MISSION: QAPod – Execute E2E Test Scenarios

🧾 TASK YAML:
task_id: 3.2_execute_e2e_scenarios
pod: QAPod
description: Execute full E2E scenarios defined in the test plan and document results
inputs:
  - test/e2e/e2e_test_plan.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

Use the GitHub File Tool to read the full E2E test plan.

Then:
1. Execute all defined E2E scenarios
2. For each scenario, log:
   - Scenario ID
   - Status (Passed / Failed / Blocked)
   - Actual results and screenshots/logs
   - Environment used
   - Issues encountered (if any)
3. Save structured results to `test/e2e/e2e_test_results.md`
```
