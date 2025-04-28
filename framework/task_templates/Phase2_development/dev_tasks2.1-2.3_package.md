# 📁 task_templates/iterative/2.1_to_2.3_batch

This file contains standardized task templates for Iterative Development Phase tasks 2.0 to 2.3 based on the AI-native operating system.

---


## 🧾 Task 2.1 – Design Feature and Tech Spec
```yaml
template: true

tasks:
  2.1_design_feature_and_tech_spec:
    description: For each assigned feature, draft a detailed technical specification
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/2.1_design_feature_and_tech_spec.txt
    inputs:
      - docs/features/feature_list.md
    outputs:
      - docs/specs/spec_<feature_id>.md
    feedback_file: .logs/feedback/2.1_design_feature_and_tech_spec.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00
```

---

## 🧾 Task 2.2 – Build and Test Feature Patch (DevPod)
```yaml
template: true

tasks:
  2.2_build_and_patch:
    description: Build the feature based on the approved spec, implement or update source and test files, run unit tests, update the spec if needed, and generate a patch
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/2.2_build_and_patch.txt
    inputs:
      - docs/specs/spec_<feature_id>.md
      - standards.md
      - solution_overview.md
    outputs:
      - src/feature_<feature_id>/**/*       # New or updated source code
      - tests/feature_<feature_id>/**/*     # Corresponding unit tests
      - docs/specs/spec_<feature_id>.md     # Updated spec (e.g., status, test plan)
      - .patches/patch_<timestamp>.diff     # Final patch file
    feedback_file: .logs/feedback/2.2_build_and_patch.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00
```

---

## 🧾 Task 2.3 – QA Review and Test Feature
```yaml
template: true

tasks:
  2.3_qa_review_feature:
    description: Perform QA review of the implemented feature, define test plan and cases, run tests, and document results aligned to acceptance criteria
    pod_owner: QAPod
    status: pending
    prompt: prompts/qa/2.3_qa_review_feature.txt
    inputs:
      - docs/specs/spec_<feature_id>.md
      - src/feature_<feature_id>/**/*
      - tests/feature_<feature_id>/**/*
      - docs/qa/acceptance_matrix.md
    outputs:
      - test/feature_<feature_id>/qa_test_plan.md
      - test/feature_<feature_id>/qa_test_cases.md
      - test/feature_<feature_id>/qa_test_results.md
      - docs/qa/acceptance_matrix.md
    feedback_file: .logs/feedback/2.3_qa_review_feature.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T12:00:00
    updated_at: 2025-04-22T12:00:00
```

---

## 🧠 memory.yaml (templates)
```yaml
template: true

project_goals:
  - path: docs/project_goals.md
    file_type: markdown
    description: Describes overall project goals and vision
    tags: [project_goals, planning]
    pod_owner: Human
    created_date: 2025-04-22
    last_updated_by: Human
    last_update_date: 2025-04-22

feature_list:
  - path: docs/features/feature_list.md
    file_type: markdown
    description: List of features and their metadata for implementation
    tags: [features, planning]
    pod_owner: DevPod
    created_date: 2025-04-22
    last_updated_by: DevPod
    last_update_date: 2025-04-22

pod_assignments:
  - path: docs/pods/pod_assignments.md
    file_type: markdown
    description: Mapping of features to assigned pods
    tags: [pods, team_structure]
    pod_owner: DevPod
    created_date: 2025-04-22
    last_updated_by: DevPod
    last_update_date: 2025-04-22

specs:
  - path: docs/specs/spec_<feature_id>.md
    file_type: markdown
    description: Technical specification for each feature
    tags: [specs, features, architecture]
    pod_owner: DevPod
    created_date: 2025-04-22
    last_updated_by: DevPod
    last_update_date: 2025-04-22

acceptance_matrix:
  - path: docs/qa/acceptance_matrix.md
    file_type: markdown
    description: QA matrix containing test cases and acceptance criteria
    tags: [qa, testing, acceptance]
    pod_owner: QAPod
    created_date: 2025-04-22
    last_updated_by: QAPod
    last_update_date: 2025-04-22
```

---

## 🧠 Prompt Templates (PoC-style)

### 2.1 Design Feature and Tech Spec
```markdown
🎯 POD MISSION: DevPod – Design Feature and Tech Spec

🧾 TASK YAML:
task_id: 2.1_design_feature_and_tech_spec
pod: DevPod
description: For each assigned feature, draft a detailed technical specification
inputs:
  - docs/features/feature_list.md

📁 MEMORY:
- path: docs/features/feature_list.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool to retrieve the list of assigned features.

Then:

# 📄 AI-Native Feature Tech Spec Instructions

For each feature assigned to a `DevPod`, draft a **technical specification** that clearly communicates what will be built, how it fits the overall architecture, and how it adheres to project standards.

These specs serve both **upfront planning** and **post-delivery traceability**.

---

## ✅ 1. 📋 Spec Metadata
Capture key identifiers and authorship details:

- `spec_id`: Unique identifier for this tech spec  
- `feature_id`: Related feature or epic ID  
- `title`: Descriptive name of the feature  
- `description`: What this feature does and why it matters  
- `author`: Person or pod responsible  
- `status`: Draft, In Review, Approved, Implemented  
- `created_at`: Date created  
- `last_updated_at`: Date last updated  

---

## ✅ 2. 🔧 Functional Overview

- `inputs`: Key inputs (e.g., user actions, API calls, tool outputs, prompts)  
- `outputs`: What the feature produces (e.g., UI response, file, DB entry, LLM output)  
- `user_roles`: Which user roles interact with or are impacted by this feature  
- `use_cases`: List of common usage scenarios or flows  
- `acceptance_criteria`: What conditions define "done"  

---

## ✅ 3. 🧱 Architecture Alignment

- `component_location`: Where this fits in the architecture (e.g., Streamlit UI, FastAPI backend, LLM agent, tool interface)  
- `interfaces`: APIs, tools, memory models, or external services this connects to  
- `data_flow`: Brief diagram or narrative of how data moves through the system  
- `data_model`: JSON/YAML schema or explanation of key data structures  
- `llm_usage`: Where/how LLMs are used (e.g., classification, tool dispatch, generation)  
- `tool_calls`: Any tool actions this feature uses (including OpenAPI, search, validation, etc.)

---

## ✅ 4. 🧑‍🎨 UI & UX Considerations (if applicable)

- `ui_details`: Wireframes, screen IDs, or Figma links  
- `user_flow`: Where the feature appears in the end-to-end journey  
- `accessibility_notes`: Any WCAG or usability considerations  
- `error_states`: How the UI handles edge cases or failures  

---

## ✅ 5. ⚙️ Dev Standards & Non-Functionals

- `testing_plan`: Unit tests, mocks, LLM behavior tests, etc.  
- `logging_plan`: What should be logged and where (inputs, outputs, tool errors, thoughts)  
- `performance_notes`: Any latency, load time, or model cost considerations  
- `security_notes`: Data sensitivity, API protection, access control  
- `compliance_notes`: If this feature impacts auditability, privacy, etc.  

---

## ✅ 6. 🔗 Dependencies & Integration

- `dependencies`: Upstream or downstream features required  
- `feature_flags`: Whether this should be gated or staged  
- `migration_notes`: Any required updates to data, prompts, or tooling  
- `deployment_considerations`: Rollout plan, versioning, or timing  

---

## ✅ 7. 📌 Review Checklist (Before Implementation)

- [ ] Aligned with `solution_overview.md`  
- [ ] Follows `standards.md` (folder structure, logging, testing, prompts, etc.)  
- [ ] Accepted by Product / Tech Lead  
- [ ] Test plan approved  
- [ ] DevPod ready to begin work  

---

Save each spec to:  
```
docs/specs/spec_<feature_id>.md
```

Tag open questions with `> [QUESTION]` and assumptions with `> [ASSUMPTION]` for team review.

Let me know if you'd like this exported as a reusable `.md` file or pre-filled YAML template!
```
### 2.2 Build and Patch
```markdown
🎯 POD MISSION: DevPod – Build Feature and Generate Patch

🧾 TASK YAML:
task_id: 2.2_build_and_patch
pod: DevPod
description: Build feature based on spec, test, then generate patch
inputs:
  - docs/specs/spec_<feature_id>.md

📁 MEMORY:
- path: docs/specs/spec_<feature_id>.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use GitHub File Tool to retrieve spec. Use patch generation tool to create `.diff` file.

Then:

# 🛠️ DevPod Feature Build Instructions

These are the standardized steps for DevPods implementing a feature based on an approved tech spec.

---

## ✅ 1. Review and Prepare

- Confirm the tech spec (`docs/specs/<feature_id>_spec.md`) is:
  - In `Approved` status
  - Aligned with the current solution architecture and standards
- Clarify any open `> [QUESTION]` or `> [ASSUMPTION]` blocks in the spec

---

## ✅ 2. Implement the Feature

### 🔧 a. Update or Create Code Files

- For **new functionality**:
  - Create new files in `src/feature_<feature_id>/`  
  - Follow naming conventions from `standards.md`  
- For **modifying existing files**:
  - Use clear comments and minimal diffs  
  - Ensure no breaking changes  
  - If changing shared modules, notify affected pods and add tests for all impacted code paths

### 🧪 b. Add Unit Tests

- Create or update test files under `tests/feature_<feature_id>/`  
- Each test file should:
  - Follow the structure in `standards.md`
  - Validate both expected and edge case behaviors
  - Include coverage for:
    - Function/method logic
    - LLM input/output validation (if applicable)
    - Tool/API invocation responses

- Optional: link or document tests in the tech spec (`testing_plan` section)

---

## ✅ 3. Test the Feature Locally

- Run the full test suite:
  ```
  pytest tests/feature_<feature_id>/
  ```
- Confirm all relevant scenarios pass
- If applicable, manually test UI or interaction flows

---

## ✅ 4. Update the Tech Spec (Post-Build)

- In `docs/specs/<feature_id>_spec.md`, update:
  - `status`: `Implemented` or `Merged`  
  - `last_updated_at`: Current timestamp  
  - `testing_plan`: Final test coverage summary  
  - `deployment_considerations`: Any new learnings or changes  
  - Add a `> [LESSON]` or `> [FOLLOW-UP]` note if applicable

---

## ✅ 5. Prepare and Save Patch

Once the feature is approved by the human lead:

### 📋 Patch Metadata
- `patch_id`: e.g., `patch_<timestamp>`  
- `feature_id`: Corresponding feature  
- `files_changed`: List of modified/added files  
- `test_results`: Summary of passed tests  
- `created_by`: DevPod author  
- `created_at`: Timestamp of patch creation

### 📂 Save Files
- ✅ Code: `src/feature_<feature_id>/`  
- ✅ Tests: `tests/feature_<feature_id>/`  
- ✅ Patch: `.patches/patch_<timestamp>.diff`  

Generate the patch:
```bash
git diff > .patches/patch_<timestamp>.diff
```

---

## 📌 Final Notes

- Validate that logs, prompts, and configs follow `standards.md`  
- Tag any gaps in `solution_overview.md` or `standards.md` for future iteration  
- Once committed, notify the human lead for final merge or release planning
```
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
Use the GitHub File Tool to retrieve:
- The updated tech spec to validate `acceptance_criteria` and `testing_plan`  
- Source and test files to verify behavior  
- The acceptance matrix to ensure traceability

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
```

