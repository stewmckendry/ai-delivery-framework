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