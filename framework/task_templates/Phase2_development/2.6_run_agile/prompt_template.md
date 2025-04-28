### 2.6 Prompt Template

```markdown
🎯 POD MISSION: WoWPod – Run Agile Rituals & Capture Metrics

🧾 TASK YAML:
task_id: 2.7_agile_metrics  
pod: WoWPod  
description: Facilitate agile rituals for the iteration, analyze delivery metrics, update velocity and burndown tracking, and log feedback on process strengths and gaps

📁 MEMORY:
- path: .logs/feedback/2.*.md  
  repo: stewmckendry/ai-delivery-framework  
- path: metrics/metrics.yaml  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then:

---

### ✅ Rituals & Insights

1. **Facilitate Retrospective**
   - Identify what went well, what didn’t, and what can be improved  
   - Capture:
     - Highlights or wins
     - Pain points or blockers
     - Communication or tooling issues
     - Feedback from DevPod, QAPod, and ResearchPod  
   - Summarize findings in:
     ✅ `docs/rituals/retrospective.md`

---

### 📈 Metrics Review

2. **Update Velocity Metrics**
   - Read `metrics.yaml` to extract:
     - Planned vs. completed tasks (per feature, pod, or sprint)
     - Number of patches delivered
     - Average patch review cycle time  
   - Write summary to:
     ✅ `metrics/velocity.md`  
   - Include tables, charts, or trend summaries where useful

3. **Update Burndown Chart**
   - Analyze task statuses over time (e.g., `done`, `pending`, `blocked`)  
   - Create a timeline showing cumulative task completion  
   - Write to:
     ✅ `metrics/burndown.md`

---

### 🧠 Process Health Logging

4. **Log Process Gaps and Suggestions**
   - For any systemic issues discovered (e.g., tool confusion, unclear specs, poor test coverage):  
     - Create entries in `feedback_file` using this format:

📋 **Process Feedback Metadata**
- `type`: [gap, blocker, improvement, question]  
- `related_task_id`: e.g., `2.2_build_and_patch`  
- `summary`: What happened  
- `recommendation`: Suggested fix or experiment  
- `reported_by`: Pod or person  
- `created_at`: Timestamp

---

📌 Final Notes:
- Tag any open team-wide WoW questions with `> [WOW-FOLLOW-UP]`  
- Notify the human lead if recommendations require backlog changes or cross-pod coordination  

```