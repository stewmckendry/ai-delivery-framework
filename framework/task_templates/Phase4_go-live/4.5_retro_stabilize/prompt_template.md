### 4.5 Prompt Template
```markdown
🎯 POD MISSION: WoWPod – Facilitate Go-Live Retro

🧾 TASK YAML:
task_id: 4.5_go_live_retro
pod: WoWPod
description: Host a go-live retro and document stabilization feedback
inputs:
  - .logs/deployments/go_live_log.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Review key moments, blockers, wins from go live
2. Capture notes and mitigation ideas
3. Save output to `docs/rituals/go_live_retro.md`
```
