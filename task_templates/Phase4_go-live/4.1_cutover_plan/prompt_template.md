### 4.1 Prompt Template
```markdown
🎯 POD MISSION: DeliveryPod – Create Cutover Plan

🧾 TASK YAML:
task_id: 4.1_create_cutover_plan
pod: DeliveryPod
description: Define a clear and time-bound cutover checklist and go-live plan
inputs:
  - docs/deployment/deployment_guide.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Review deployment guide and identify:
   - Final pre-go-live tasks
   - Required validation or smoke tests
   - Responsible roles and fallback actions
2. Organize into a checklist and timeline
3. Include contingencies, rollback plan, and check-in cadence
4. Save to `docs/release/cutover_checklist.md`
```