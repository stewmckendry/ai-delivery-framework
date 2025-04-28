### 4.3 Prompt Template
```markdown
🎯 POD MISSION: DevPod – Execute Go Live

🧾 TASK YAML:
task_id: 4.3_go_live_deployment
pod: DevPod
description: Execute deployment steps into production, following the cutover checklist
inputs:
  - docs/release/cutover_checklist.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Follow cutover sequence exactly as outlined
2. Log command output, issues, and timestamps
3. Save the deployment log to `.logs/deployments/go_live_log.md`
```
