### 2.5 Prompt Template

```markdown
🎯 POD MISSION: ResearchPod – Resolve Open Questions and Gaps

🧾 TASK YAML:
task_id: 2.5_research_assist  
pod: ResearchPod  
description: Investigate unresolved technical or domain-specific questions raised during the build, QA, or testing cycle. Summarize findings as research spikes for future implementation or discussion.

📁 MEMORY:
- path: .logs/feedback/2.x_*.md  
  repo: stewmckendry/ai-delivery-framework  
- path: docs/specs/spec_<feature_id>.md  
  repo: stewmckendry/ai-delivery-framework  
- path: docs/qa/acceptance_matrix.md  
  repo: stewmckendry/ai-delivery-framework  

📡 TOOL USE:
Use the GitHub File Tool’s POST /batch-files endpoint to fetch all inputs.

Then:
---

### 🔍 Research Instructions

1. **Identify Research Topics**
   - Scan files for open markers:  
     - `> [QUESTION]` – unresolved technical question  
     - `> [GAP]` – missing decision or design element  
     - `> [FOLLOW-UP]` – flagged area needing exploration  
   - Prioritize those impacting architecture, delivery, or quality

2. **Conduct Focused Investigation**
   - Use trusted sources (docs, repos, articles, model outputs, POCs)  
   - Compare trade-offs if evaluating tools, libraries, or model techniques  
   - Where helpful, provide code examples or structured comparisons  
   - If no clear answer exists, frame considerations or next steps

3. **Document Your Findings**

Create a Markdown spike file:
✅ `docs/research/spikes/<topic>.md`

Include the following:

📋 **Research Spike Metadata**
- `spike_id`: Unique identifier (e.g., `spike_20250422_memory_models`)  
- `related_feature_id`: Optional – link to the feature or task  
- `question`: What was being investigated  
- `summary`: Key findings and implications  
- `recommendations`: Proposed actions, decisions, or options  
- `confidence_level`: High / Medium / Low  
- `research_by`: Pod author or name  
- `created_at`: Timestamp

---

📌 Final Step:
- Update the related spec or acceptance matrix with a summary or resolution link  
- Leave a note in `feedback_file` indicating what was resolved and where the spike is saved  
- If additional work is required, propose a follow-up task to the human lead
```

---