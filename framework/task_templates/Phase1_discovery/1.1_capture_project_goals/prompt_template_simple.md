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
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. 

Then:

1. **Summarize the Project in 3–4 Bullet Points**
   - What are we building?
   - Who is it for?
   - Why does it matter?
   - What does success look like?

2. **Define 2–3 Clear Goals**  
   For each goal, provide the following details (keep it short and practical):

   - `title:` A brief name for the goal  
   - `description:` What are we trying to achieve?  
   - `why_it_matters:` Why is this goal important?  
   - `success_criteria:` How will we know we succeeded?  

   *Optional (if useful):*
   - `priority:` High / Medium / Low  
   - `timeframe:` e.g., MVP, by end of week, short-term  

3. **Spot and Flag Gaps**
   - Are any goals unclear or missing?
   - Are we assuming anything we should check?

4. **Propose a `docs/project_goals.md` in Markdown Format**
   - Generate a clean, readable markdown file summarizing the above.