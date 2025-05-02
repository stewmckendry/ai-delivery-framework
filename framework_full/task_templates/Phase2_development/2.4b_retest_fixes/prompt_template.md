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
