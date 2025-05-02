### Task 1.3 – Break Into Features
```markdown
🎯 POD MISSION: DevPod – Break Into Features

🧾 TASK YAML:
task_id: 1.3_break_into_features
pod: DevPod
description: Analyze project scope and break it into features, experiments, or hypotheses
inputs:
  - docs/project_goals.md

📁 MEMORY:
- path: docs/project_goals.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the project goals.

Then:
1. Summarize and refine the project scope into 3–7 features or hypotheses
2. For each proposed feature, provide the following where applicable:

📋 Core Metadata
- `feature_id`: Unique identifier
- `title`: Short, descriptive name of the feature
- `description`: What the feature does, user problem it solves
- `status`: Current state (e.g., Draft, In Progress, Done, Blocked)
- `type`: Feature, Enhancement, Bugfix, Tech Debt, Spike
- `priority`: Importance relative to other work (e.g., P0–P3)
- `tags`: Keywords for filtering (e.g., "auth", "mobile", "payments")
- `created_by`: Who added the feature
- `created_at`: Date the feature was logged

🧠 Product & UX Context
- `user_story`: Value from the user's perspective (e.g., “As a user, I want to...”) 
- `personas`: Target user types/personas
- `acceptance_criteria`: Conditions that define “done”
- `mockups`: Link to designs (e.g., Figma, images)
- `journey_stage`: Where this fits in the user journey (e.g., Onboarding, Retention)

🛠 Delivery Context
- 'epic:' Larger initiative or Epic this belongs to
- 'dependencies:' Blocking or related features
- 'estimated_effort:' Story points or t-shirt size (e.g., S, M, L)
- 'tech_owner:' Dev team member responsible
- 'product_owner:' PM or stakeholder lead
- 'repo:' Codebase or directory this touches
- 'test_cases:' Tests to validate behavior
- 'qa_owner:' Responsible for testing
- 'release_target:' Sprint, milestone, or version

✅ Post-Delivery Insights (Optional)
- 'metrics:' KPIs or outcomes to measure success
- 'release_notes:' What was announced or documented externally
- 'retro_notes:' Lessons learned during delivery

3. Identify any ambiguities, unknowns, or decisions to confirm with the human
4. Propose markdown-formatted outputs for `docs/features/feature_*.md`