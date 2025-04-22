# 🧪 PoC Test Pack – Iterative Tasks 2.1 to 2.3

This test pack supports proof-of-concept runs for Tasks 2.1, 2.2, and 2.3 using the Memory Pod GPT + GitHub Tool integration.

---

## ✅ Objectives by Task

### 🧾 Task 2.1 – Design Feature and Tech Spec
**Goal:** Create a complete tech spec for each assigned feature using the AI-native template.

**Files:**
- `docs/features/feature_list.md`
- `docs/specs/spec_<feature_id>.md`

**Prompt:** Use the full template from `prompts/dev/2.1_design_feature_and_tech_spec.txt`

**Expected Outputs:**
- A well-structured tech spec with all 7 metadata sections
- Tagged questions or assumptions for human follow-up

---

### 🧾 Task 2.2 – Build and Patch
**Goal:** Implement the feature according to spec, write tests, update the spec post-build, and generate a patch.

**Files:**
- `docs/specs/spec_<feature_id>.md`
- `src/feature_<feature_id>/**/*`
- `tests/feature_<feature_id>/**/*`
- `.patches/patch_<timestamp>.diff`

**Prompt:** Use the full template from `prompts/dev/2.2_build_and_patch.txt`

**Expected Outputs:**
- Source and test code with unit test coverage
- Updated spec file (status = Implemented)
- Patch file with correct diff output

---

### 🧾 Task 2.3 – QA Review and Test Feature
**Goal:** QA Pod writes test plan, defines test cases, validates the implementation, and documents test results.

**Files:**
- `docs/specs/spec_<feature_id>.md`
- `tests/feature_<feature_id>/**/*`
- `src/feature_<feature_id>/**/*`
- `test/feature_<feature_id>/qa_test_plan.md`
- `test/feature_<feature_id>/qa_test_cases.md`
- `test/feature_<feature_id>/qa_test_results.md`
- `docs/qa/acceptance_matrix.md`

**Prompt:** Use the full template from `prompts/qa/2.3_qa_review_feature.txt`

**Expected Outputs:**
- Completed test plan and test case definitions
- Logged QA results using structured metadata
- Updated acceptance matrix

---

## 🔁 Workflow
1. Run each prompt via DevPod or QAPod
2. Use the GitHub File Tool to fetch required inputs
3. Allow GPT to generate drafts based on prompt instructions
4. Save generated files (manual commit or patch tool)
5. Log feedback to `.logs/feedback/task_id.md`

---

## 📁 Supporting File Checklist
Make sure these are committed or created during testing:
- `docs/features/feature_list.md`
- `docs/specs/spec_<feature_id>.md`
- `src/feature_<feature_id>/`
- `tests/feature_<feature_id>/`
- `test/feature_<feature_id>/qa_test_plan.md`
- `test/feature_<feature_id>/qa_test_cases.md`
- `test/feature_<feature_id>/qa_test_results.md`
- `docs/qa/acceptance_matrix.md`
- `.patches/patch_<timestamp>.diff`

---

Let me know if you want to add a feedback form, metrics tracker, or validation script for this test pack.

