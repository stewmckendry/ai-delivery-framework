# 📁 task_templates/phase3_end_to_end_testing.md

This file contains standardized `task.yaml`, `prompt_template.md`, and `memory.yaml` templates for Phase 3 – End-to-End Testing.

---

## 🧾 Task 3.1 – Define E2E Test Plan
```yaml
template: true

tasks:
  3.1_define_e2e_test_plan:
    description: Define a comprehensive end-to-end (E2E) test plan covering full user flows, edge cases, and systems integration
    pod_owner: QAPod
    status: pending
    prompt: prompts/qa/3.1_define_e2e_test_plan.txt
    inputs:
      - docs/features/feature_list.md
      - docs/qa/acceptance_matrix.md
      - docs/specs/spec_*.md
    outputs:
      - test/e2e/e2e_test_plan.md
    feedback_file: .logs/feedback/3.1_define_e2e_test_plan.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T13:00:00
    updated_at: 2025-04-22T13:00:00
```

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

---

## 🧾 Task 3.2 – Execute E2E Scenarios
```yaml
template: true

tasks:
  3.2_execute_e2e_scenarios:
    description: Run defined E2E test scenarios and log outcomes for each test case, noting any failures or inconsistencies
    pod_owner: QAPod
    status: pending
    prompt: prompts/qa/3.2_execute_e2e_scenarios.txt
    inputs:
      - test/e2e/e2e_test_plan.md
    outputs:
      - test/e2e/e2e_test_results.md
    feedback_file: .logs/feedback/3.2_execute_e2e_scenarios.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T13:00:00
    updated_at: 2025-04-22T13:00:00
```

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

---

## 🧾 Task 3.3 – Fix Bugs and Update Implementation
```yaml
template: true

tasks:
  3.3_fix_bugs_e2e:
    description: Address issues uncovered in E2E testing and update source code, tests, and documentation as needed
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/3.3_fix_bugs_e2e.txt
    inputs:
      - test/e2e/e2e_test_results.md
    outputs:
      - src/**/*
      - tests/**/*
      - docs/specs/spec_*.md
      - .patches/patch_<timestamp>.diff
    feedback_file: .logs/feedback/3.3_fix_bugs_e2e.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T13:00:00
    updated_at: 2025-04-22T13:00:00
```

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

## 🧾 Task 3.4 – Coordinate E2E Review or Demo
```yaml
template: true

tasks:
  3.4_coordinate_e2e_demo:
    description: Organize and document an end-to-end walkthrough, review, or demo of key app workflows
    pod_owner: WoWPod
    status: pending
    prompt: prompts/wow/3.4_coordinate_e2e_demo.txt
    inputs:
      - test/e2e/e2e_test_results.md
    outputs:
      - docs/reviews/e2e_review_notes.md
    feedback_file: .logs/feedback/3.4_coordinate_e2e_demo.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T13:00:00
    updated_at: 2025-04-22T13:00:00
```

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

---

## 🧾 Task 3.5 – Track Issues and Finalize Quality Metrics
```yaml
template: true

tasks:
  3.5_finalize_quality_metrics:
    description: Track unresolved issues and summarize final quality metrics, including test coverage, pass rates, and defects
    pod_owner: DeliveryPod
    status: pending
    prompt: prompts/delivery/3.5_finalize_quality_metrics.txt
    inputs:
      - test/e2e/e2e_test_results.md
      - metrics/metrics.yaml
    outputs:
      - metrics/final_quality_summary.md
    feedback_file: .logs/feedback/3.5_finalize_quality_metrics.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T13:00:00
    updated_at: 2025-04-22T13:00:00
```

### 3.5 Prompt Template
```markdown
🎯 POD MISSION: DeliveryPod – Finalize Quality Metrics

🧾 TASK YAML:
task_id: 3.5_finalize_quality_metrics
pod: DeliveryPod
description: Track unresolved issues and summarize final metrics across E2E testing
inputs:
  - test/e2e/e2e_test_results.md
  - metrics/metrics.yaml

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Use GitHub File Tool to retrieve inputs.

Then:
1. Calculate:
   - Total test scenarios run
   - Pass/fail/block rates
   - Unresolved issue count
   - P0 defect count
   - QA sign-off ratio
2. Write up final metrics summary
3. Save report to `metrics/final_quality_summary.md`
```

---

Let me know when you're ready for stub files, test pack, or YAML scaffolds!

