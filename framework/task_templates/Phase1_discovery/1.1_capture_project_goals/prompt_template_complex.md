🎯 POD MISSION: DevPod – Capture Project Goals

🧾 TASK YAML:
task_id: 1.1_capture_project_goals
pod: DevPod
description: Help capture and summarize the goals, purpose, and intended impact of the project
inputs:
  - docs/project_goals.md

📁 MEMORY:
- path: docs/project_goals.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Summarize and refine the goals in 3–5 bullet points:
   - What is the project?
   - Who is it for?
   - Why does it matter?
   - What outcomes are we aiming for?
2. Describe each goal with the following metadata if available:

- 'goal_id:' Unique identifier for the goal (e.g., goal_001)
- 'title:' Unique identifier for the goal (e.g., goal_001)
- 'description:' Clear explanation of what the goal aims to achieve
- 'why_it_matters:' Strategic reason or user problem this goal addresses
- 'success_criteria:' How you’ll know the goal has been achieved (measurable or observable outcomes)
- 'priority:' Importance relative to other goals (e.g., High, Medium, Low)
- 'alignment:' Linked product vision, initiative, or business objective
- 'time_horizon:' Expected timeframe (e.g., short-term, 2025 Q2, MVP, long-term)
- 'related_personas:' User roles most impacted by this goal
- 'dependencies:' Other goals or features this depends on
- 'risk_factors:' Known risks or blockers to achieving this goal
- 'status:' Current state (e.g., Proposed, In Progress, Achieved, Abandoned)
- 'tags:' Keywords or themes (e.g., onboarding, retention, data privacy)
- 'created_by:' Who defined the goal
- 'created_at:' When it was documented
- 'last_updated_by:' Who last modified it
- 'last_updated_at:' Date of last update

2. Identify any ambiguities or gaps to discuss with the human
3. Propose a refined version of `docs/project_goals.md` formatted in markdown