### 3.4 Prompt Template
```markdown
🎯 POD MISSION: WoWPod – Coordinate E2E Review or Demo

🧾 TASK YAML:
task_id: 3.4_coordinate_e2e_demo
pod: WoWPod
description: Plan and document a coordinated end-to-end walkthrough or demo session
inputs:
  - test/e2e/e2e_test_results.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

Use the GitHub File Tool to access E2E results.

Then:
1. Review test outcomes and pick representative flows
2. Document walkthrough steps or demo agenda
3. Include user roles, environment, expected transitions
4. Note any feedback or action items
5. Save summary to `docs/reviews/e2e_review_notes.md`
```
