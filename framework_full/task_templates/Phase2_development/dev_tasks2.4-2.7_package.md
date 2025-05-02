# 📁 task\_templates/iterative/2.4\_to\_2.8\_batch

This file contains standardized task templates, memory.yaml entries, and prompt templates for Iterative Development Phase tasks 2.4 to 2.8.

---

## 🧾 Task 2.4a – Fix Bugs from QA

```yaml
template: true

tasks:
  2.4a_fix_bugs_from_qa:
    description: Address bugs identified by QAPod during QA review, apply code and test fixes, validate with local test runs, and update spec and patch
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/2.4a_fix_bugs_from_qa.txt
    inputs:
      - test/feature_<feature_id>/qa_test_results.md
      - docs/specs/spec_<feature_id>.md
    outputs:
      - src/feature_<feature_id>/**/*            # Bugfixes in feature code
      - tests/feature_<feature_id>/**/*          # Updated or added test coverage
      - docs/specs/spec_<feature_id>.md          # Updated status or test plan
      - .patches/patch_<timestamp>.diff          # Patch with bugfixes
    feedback_file: .logs/feedback/2.4a_fix_bugs_from_qa.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00

```

### 2.4a Prompt Template

````markdown
🎯 POD MISSION: DevPod – Fix Bugs from QA Review

🧾 TASK YAML:
task_id: 2.4a_fix_bugs_from_qa  
pod: DevPod  
description: Address bugs identified by QAPod during QA review, apply code and test fixes, validate with test runs, and submit an updated patch

📁 MEMORY:
- path: test/feature_<feature_id>/qa_test_results.md  
  repo: stewmckendry/ai-delivery-framework  
- path: docs/specs/spec_<feature_id>.md  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

---

### 🛠️ Dev Instructions

1. **Review QA Failures**
   - Identify all test cases with `status: Failed` or `Blocked`
   - Review `linked_criteria` and `actual_result` for diagnosis

2. **Fix Code and Test Issues**
   - Update `src/feature_<feature_id>/` to resolve bugs  
   - Modify or add unit tests under `tests/feature_<feature_id>/` to confirm fixes  
   - Be cautious when editing shared files — avoid regressions  
   - Clearly comment or document all major fixes

3. **Rerun Local Tests**
   ```bash
   pytest tests/feature_<feature_id>/
Update the Spec
Update status, testing_plan, or > [FOLLOW-UP] notes in spec_<feature_id>.md
Update last_updated_at in the metadata block
Generate Patch
Save your changes
Create a new patch file:
git diff > .patches/patch_<timestamp>.diff
📥 Final Deliverables:

Updated source files: src/feature_<feature_id>/
Updated tests: tests/feature_<feature_id>/
Revised spec: docs/specs/spec_<feature_id>.md
Patch file: .patches/patch_<timestamp>.diff

Let me know if you want a companion task `2.4b_retest_fixes` for QAPod or templates for test result parsing!
````

---

## 🧾 Task 2.4b – Retest After Fixes

```yaml
template: true

tasks:
  2.4b_retest_after_fixes:
    description: Re-run previously failed or blocked test cases after DevPod fixes, confirm bug resolution, and update QA results and acceptance matrix
    pod_owner: QAPod
    status: pending
    prompt: prompts/qa/2.4b_retest_after_fixes.txt
    inputs:
      - test/feature_<feature_id>/qa_test_results.md
      - src/feature_<feature_id>/**/*
      - tests/feature_<feature_id>/**/*
      - docs/qa/acceptance_matrix.md
    outputs:
      - test/feature_<feature_id>/qa_test_results.md         # Updated test case statuses
      - docs/qa/acceptance_matrix.md                         # Final validation record
    feedback_file: .logs/feedback/2.4b_retest_after_fixes.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00

```

### 2.4b Prompt Template

```markdown
🎯 POD MISSION: QAPod – Retest Feature After Bug Fixes

🧾 TASK YAML:
task_id: 2.4b_retest_after_fixes  
pod: QAPod  
description: Re-run previously failed or blocked test cases, confirm issues are resolved, and update test results and final acceptance status

📁 MEMORY:
- path: test/feature_<feature_id>/qa_test_results.md  
  repo: stewmckendry/ai-delivery-framework  
- path: docs/qa/acceptance_matrix.md  
  repo: stewmckendry/ai-delivery-framework  
- path: src/feature_<feature_id>/**/*  
  repo: stewmckendry/ai-delivery-framework  
- path: tests/feature_<feature_id>/**/*  
  repo: stewmckendry/ai-delivery-framework  


📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then: 
---

### ✅ QA Retest Instructions

1. **Identify Retest Scope**
   - Review all test cases with `status: Failed` or `Blocked`  
   - Note any `linked_criteria` and related bug notes  

2. **Re-execute Affected Tests**
   - Manually verify behavior or re-run automated tests  
   - Confirm bug fixes as implemented by DevPod  
   - Optionally, run regression on any impacted flows

3. **Validate New Test Coverage**
   - Check for new test cases or edge conditions added by DevPod  
   - Validate they run and cover expected behaviors

4. **Update QA Artifacts**

Update each relevant test case in:

✅ `test/feature_<feature_id>/qa_test_results.md`  
- Update `status`: e.g., Failed → Passed  
- Add notes to `actual_result` if needed  
- Timestamp the update (`run_at`)

Update corresponding criteria in:

✅ `docs/qa/acceptance_matrix.md`  
- Confirm test case linkage  
- Mark acceptance status as `Validated` if all tests pass  
- Add `> [FOLLOW-UP]` notes if further clarification is needed

---

📌 Final Notes:
- Confirm feature is fully validated across functional and edge cases  
- If any failures remain, update the test result and notify DevPod  
- Flag any spec gaps, test coverage issues, or test data concerns for review

```

---

## 🧾 Task 2.5 – Research Support for Unresolved Questions

```yaml
template: true

tasks:
  2.5_research_assist:
    description: Investigate and summarize findings for unresolved technical, architectural, or domain-specific questions raised during the feature cycle
    pod_owner: ResearchPod
    status: pending
    prompt: prompts/research/2.5_research_assist.txt
    inputs:
      - .logs/feedback/2.x_*.md
      - docs/specs/spec_<feature_id>.md
      - docs/qa/acceptance_matrix.md
    outputs:
      - docs/research/spikes/<topic>.md
    feedback_file: .logs/feedback/2.5_research_assist.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00
```

### 2.5 Prompt Template

```markdown
🎯 POD MISSION: ResearchPod – Resolve Open Questions and Gaps

🧾 TASK YAML:
task_id: 2.5_research_assist  
pod: ResearchPod  
description: Investigate unresolved technical or domain-specific questions raised during the build, QA, or testing cycle. Summarize findings as research spikes for future implementation or discussion.

📁 MEMORY:
- path: .logs/feedback/2.x_*.md  
  repo: stewmckendry/ai-delivery-framework  
- path: docs/specs/spec_<feature_id>.md  
  repo: stewmckendry/ai-delivery-framework  
- path: docs/qa/acceptance_matrix.md  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then:
---

### 🔍 Research Instructions

1. **Identify Research Topics**
   - Scan files for open markers:  
     - `> [QUESTION]` – unresolved technical question  
     - `> [GAP]` – missing decision or design element  
     - `> [FOLLOW-UP]` – flagged area needing exploration  
   - Prioritize those impacting architecture, delivery, or quality

2. **Conduct Focused Investigation**
   - Use trusted sources (docs, repos, articles, model outputs, POCs)  
   - Compare trade-offs if evaluating tools, libraries, or model techniques  
   - Where helpful, provide code examples or structured comparisons  
   - If no clear answer exists, frame considerations or next steps

3. **Document Your Findings**

Create a Markdown spike file:
✅ `docs/research/spikes/<topic>.md`

Include the following:

📋 **Research Spike Metadata**
- `spike_id`: Unique identifier (e.g., `spike_20250422_memory_models`)  
- `related_feature_id`: Optional – link to the feature or task  
- `question`: What was being investigated  
- `summary`: Key findings and implications  
- `recommendations`: Proposed actions, decisions, or options  
- `confidence_level`: High / Medium / Low  
- `research_by`: Pod author or name  
- `created_at`: Timestamp

---

📌 Final Step:
- Update the related spec or acceptance matrix with a summary or resolution link  
- Leave a note in `feedback_file` indicating what was resolved and where the spike is saved  
- If additional work is required, propose a follow-up task to the human lead
```

---

---

## 🧾 Task 2.6 – Run Agile Rituals & Capture Metrics

```yaml
template: true

tasks:
  2.7_agile_metrics:
    description: Facilitate agile rituals (e.g., retrospective), analyze velocity and task completion data, update delivery metrics, and log team process insights and gaps
    pod_owner: WoWPod
    status: pending
    prompt: prompts/wow/2.7_agile_metrics.txt
    inputs:
      - .logs/feedback/2.*.md
      - metrics/metrics.yaml
    outputs:
      - docs/rituals/retrospective.md
      - metrics/velocity.md
      - metrics/burndown.md
      - .logs/feedback/2.7_agile_metrics.md
    feedback_file: .logs/feedback/2.7_agile_metrics.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00
```

### 2.6 Prompt Template

```markdown
🎯 POD MISSION: WoWPod – Run Agile Rituals & Capture Metrics

🧾 TASK YAML:
task_id: 2.7_agile_metrics  
pod: WoWPod  
description: Facilitate agile rituals for the iteration, analyze delivery metrics, update velocity and burndown tracking, and log feedback on process strengths and gaps

📁 MEMORY:
- path: .logs/feedback/2.*.md  
  repo: stewmckendry/ai-delivery-framework  
- path: metrics/metrics.yaml  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then:

---

### ✅ Rituals & Insights

1. **Facilitate Retrospective**
   - Identify what went well, what didn’t, and what can be improved  
   - Capture:
     - Highlights or wins
     - Pain points or blockers
     - Communication or tooling issues
     - Feedback from DevPod, QAPod, and ResearchPod  
   - Summarize findings in:
     ✅ `docs/rituals/retrospective.md`

---

### 📈 Metrics Review

2. **Update Velocity Metrics**
   - Read `metrics.yaml` to extract:
     - Planned vs. completed tasks (per feature, pod, or sprint)
     - Number of patches delivered
     - Average patch review cycle time  
   - Write summary to:
     ✅ `metrics/velocity.md`  
   - Include tables, charts, or trend summaries where useful

3. **Update Burndown Chart**
   - Analyze task statuses over time (e.g., `done`, `pending`, `blocked`)  
   - Create a timeline showing cumulative task completion  
   - Write to:
     ✅ `metrics/burndown.md`

---

### 🧠 Process Health Logging

4. **Log Process Gaps and Suggestions**
   - For any systemic issues discovered (e.g., tool confusion, unclear specs, poor test coverage):  
     - Create entries in `feedback_file` using this format:

📋 **Process Feedback Metadata**
- `type`: [gap, blocker, improvement, question]  
- `related_task_id`: e.g., `2.2_build_and_patch`  
- `summary`: What happened  
- `recommendation`: Suggested fix or experiment  
- `reported_by`: Pod or person  
- `created_at`: Timestamp

---

📌 Final Notes:
- Tag any open team-wide WoW questions with `> [WOW-FOLLOW-UP]`  
- Notify the human lead if recommendations require backlog changes or cross-pod coordination  

```



---

## 🧾 Task 2.7 – Prepare Deployment Guide

```yaml
template: true

tasks:
  2.8_prepare_deployment_guide:
    description: Create a clear, reproducible deployment guide covering environments, configuration, tooling, and steps for deploying the current feature set
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/2.8_prepare_deployment_guide.txt
    inputs:
      - docs/specs/spec_<feature_id>.md
      - .patches/patch_<timestamp>.diff
    outputs:
      - docs/deployment/deployment_guide.md
    feedback_file: .logs/feedback/2.8_prepare_deployment_guide.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00

```

### 2.7 Prompt Template

```markdown
🎯 POD MISSION: DevPod – Prepare Deployment Guide

🧾 TASK YAML:
task_id: 2.8_prepare_deployment_guide  
pod: DevPod  
description: Create a guide to deploy the current feature set to a test, staging, or production environment, including all steps, configs, and dependencies

📁 MEMORY:
- path: docs/specs/spec_<feature_id>.md  
  repo: stewmckendry/ai-delivery-framework  
- path: .patches/patch_<timestamp>.diff  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool to retrieve:
- The finalized feature spec  
- The latest patch diff  
- Any notes on environment or infra config from earlier phases

---

### ✅ Deployment Guide Instructions

1. **Summarize Feature Deployment Context**
   - State what feature(s) this guide supports  
   - Note if this is for testing, staging, or production deployment

2. **Document Environment and Dependencies**
   - Required environment(s): `dev`, `test`, `prod`, etc.  
   - Dependencies: Python version, models, packages, container base image  
   - System-level requirements: Docker, Git, Python, etc.  
   - Required services: API keys, external tools, vector DBs, etc.

3. **List Environment Variables and Secrets**
   - Include all required env vars  
   - Label sensitive variables as `[SECRET]`  
   - Point to `.env.example` or secret manager config if applicable

4. **Define Deployment Steps**
   - **Manual Steps**:
     - Clone repo, activate env, install dependencies  
     - Run init scripts, migrations, or tests  
     - Deploy using Docker, Streamlit, FastAPI, etc.  
   - **CI/CD Steps**:
     - Trigger GitHub Action or pipeline  
     - Reference `.github/workflows/deploy.yaml` or equivalent  
     - Describe how to monitor deployment logs

5. **Include Post-Deployment Validation**
   - How to confirm deployment success (e.g., health checks, smoke tests)  
   - Where to check logs or outputs  
   - Who to notify

---

### 📥 Save Final Guide

✅ Save completed guide to:  
`docs/deployment/deployment_guide.md`

Include structured sections:
#Deployment Guide
##Feature Summary
##Environments
##Dependencies
##Environment Variables
##Deployment Steps (Manual & CI)
##Post-Deployment Checks
##Troubleshooting
---

📌 Final Notes:
- Tag any blockers or assumptions in the guide using `> [GAP]` or `> [FOLLOW-UP]`  
- If major deployment infrastructure is missing or unclear, suggest a ResearchPod spike  
- Add deployment status summary to the feedback file
```

