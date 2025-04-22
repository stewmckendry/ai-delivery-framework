### 4.4 Prompt Template
```markdown
🎯 POD MISSION: Human – Communicate Release

🧾 TASK YAML:
task_id: 4.4_announce_go_live
pod: Human
description: Announce the go-live milestone and transition responsibilities
inputs:
  - .logs/deployments/go_live_log.md

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Summarize release highlights, new capabilities, and key contributors
2. Clarify who owns what post go-live
3. Save to `docs/release/release_announcement.md`
```
