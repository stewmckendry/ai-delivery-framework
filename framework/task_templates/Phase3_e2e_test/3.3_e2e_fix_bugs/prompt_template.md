 ### 3.3 Prompt Template
```markdown
🎯 POD MISSION: DevPod – Fix Bugs from E2E Testing

🧾 TASK YAML:
task_id: 3.3_fix_bugs_e2e
pod: DevPod
description: Fix bugs found during E2E execution and update codebase and documentation
inputs:
  - test/e2e/e2e_test_results.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

Use the GitHub Tool to review test results.

Then:
1. Identify failing or blocked scenarios
2. Trace to root cause and update code or configs
3. Add or modify test coverage where applicable
4. Update spec if needed
5. Save a patch to `.patches/patch_<timestamp>.diff`
```

---