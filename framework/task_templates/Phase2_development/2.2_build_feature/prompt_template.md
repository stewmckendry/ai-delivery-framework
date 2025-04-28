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
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.
Use patch generation tool to create `.diff` file.

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