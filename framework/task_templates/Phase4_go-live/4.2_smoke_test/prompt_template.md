### 4.2 Prompt Template
```markdown
🎯 POD MISSION: QAPod – Run Final Smoke Tests

🧾 TASK YAML:
task_id: 4.2_final_smoke_tests
pod: QAPod
description: Run lightweight but critical tests in production to validate deployment readiness
inputs:
  - test/e2e/e2e_test_plan.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Select 5–10 representative test cases
2. Execute manually in the production environment
3. Log each:
   - Test ID
   - Scenario
   - Status
   - Result or error
4. Save results to `test/smoke/smoke_test_results.md`
```
