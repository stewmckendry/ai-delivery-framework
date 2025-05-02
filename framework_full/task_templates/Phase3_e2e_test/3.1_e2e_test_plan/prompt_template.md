### 3.1 Prompt Template
```markdown
🎯 POD MISSION: QAPod – Define End-to-End Test Plan

🧾 TASK YAML:
task_id: 3.1_define_e2e_test_plan
pod: QAPod
description: Define a comprehensive E2E test plan covering full user flows, edge cases, integration points, and deployment environments
inputs:
  - docs/features/feature_list.md
  - docs/qa/acceptance_matrix.md
  - docs/specs/spec_*.md

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Use the GitHub File Tool’s POST /batch-files endpoint to retrieve inputs.

Then:
1. Group features by major user flow or capability
2. Identify critical paths, cross-feature dependencies, and edge cases
3. For each E2E scenario, define:
   - Scenario ID and title
   - Preconditions
   - Test steps
   - Expected result
   - Roles involved
   - Priority (P0–P3)
   - Environment(s) required
   - Tools or mocks needed
4. Summarize known risks and areas to monitor
5. Save the plan to `test/e2e/e2e_test_plan.md`
```