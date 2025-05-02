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
