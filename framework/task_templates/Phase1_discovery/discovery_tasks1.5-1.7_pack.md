# 📁 task_templates/discovery/1.5_to_1.7_batch

This file contains standardized task templates for the final Discovery Phase tasks (1.5 to 1.7).

---

## 🧾 Task 1.5 – Research Spikes or Open Questions
```yaml
template: true

tasks:
  1.5_research_spikes:
    description: Investigate and document unresolved questions, unknowns, or tool comparisons
    pod_owner: ResearchPod
    status: pending
    prompt: prompts/research/research_spikes.txt
    inputs:
      - docs/project_goals.md
      - docs/features/feature_*.md
    outputs:
      - docs/research/spikes/spike_*.md
    feedback_file: .logs/feedback/1.5_research_spikes.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T10:00:00
    updated_at: 2025-04-22T10:00:00
```

---

## 🧾 Task 1.6 – Define Solution Architecture and Standards
```yaml
template: true

tasks:
  1.6_define_architecture_and_standards:
    description: Draft initial solution architecture and coding or design standards
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/define_architecture.txt
    inputs:
      - docs/project_goals.md
      - docs/features/feature_*.md
      - docs/research/spikes/spike_*.md
    outputs:
      - docs/architecture/solution_overview.md
      - docs/architecture/standards.md
    feedback_file: .logs/feedback/1.6_define_architecture_and_standards.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T10:00:00
    updated_at: 2025-04-22T10:00:00
```

---

## 🧾 Task 1.7 – Feedback Summary
```yaml
template: true

tasks:
  1.7_feedback_summary:
    description: Summarize chat feedback, discussion notes, and key decisions
    pod_owner: Human
    status: pending
    prompt: prompts/human/summarize_feedback.txt
    inputs:
      - .logs/feedback/*.md
    outputs:
      - .logs/feedback/1.7_feedback_summary.md
    feedback_file: .logs/feedback/1.7_feedback_summary.md
    ready: true
    done: false
    created_by: human
    created_at: 2025-04-22T10:00:00
    updated_at: 2025-04-22T10:00:00
```

---

## 🧠 memory.yaml (templates)

```yaml
template: true

research_spikes:
  - path: docs/research/spikes/spike_*.md
    repo: stewmckendry/ai-delivery-framework
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/research/spikes/spike_sample.md
    file_type: markdown
    description: Research findings and technical explorations to resolve open questions
    tags: [research, spike, investigations]
    pod_owner: ResearchPod
    created_date: 2025-04-22
    last_updated_by: Human
    last_update_date: 2025-04-22
    notes: Work-in-progress spikes to unblock feature delivery

architecture:
  - path: docs/architecture/solution_overview.md
    repo: stewmckendry/ai-delivery-framework
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/architecture/solution_overview.md
    file_type: markdown
    description: Overview of the technical architecture, patterns, and deployment
    tags: [architecture, solution_design]
    pod_owner: DevPod
    created_date: 2025-04-22
    last_updated_by: Human
    last_update_date: 2025-04-22
    notes: System-level view for reference by all pods

  - path: docs/architecture/standards.md
    repo: stewmckendry/ai-delivery-framework
    raw_url: https://raw.githubusercontent.com/stewmckendry/ai-delivery-framework/main/docs/architecture/standards.md
    file_type: markdown
    description: Code, documentation, and interface standards
    tags: [standards, architecture]
    pod_owner: ResearchPod
    created_date: 2025-04-22
    last_updated_by: Human
    last_update_date: 2025-04-22
    notes: Shared coding standards across pods
```

---

## ✨ Prompt Templates (PoC-style)

### Task 1.5 – Research Spikes or Open Questions
```markdown
🎯 POD MISSION: ResearchPod – Investigate Open Questions

🧾 TASK YAML:
task_id: 1.5_research_spikes
pod: ResearchPod
description: Investigate and document unresolved questions, unknowns, or tool comparisons
inputs:
  - docs/project_goals.md
  - docs/features/feature_*.md

📁 MEMORY:
- path: docs/project_goals.md
  repo: stewmckendry/ai-delivery-framework
- path: docs/features/feature_*.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use the GitHub File Tool to retrieve goals and feature specs.

Then:
1. Identify 2–3 open questions, risks, or decision areas
2. For each spike, provide a markdown entry:
   - Summary of the problem or unknown
   - Related features or personas
   - Research method (docs, experiments, comparisons)
   - Key findings
   - Recommendations
3. Include the following metadata for each spike where available:
  - `spike_id`: unique identifier for the spike  
  - `title`: short, descriptive name of the research topic  
  - `question`: core question(s) the spike is trying to answer  
  - `purpose`: why this spike was initiated and how it supports the product direction  
  - `scope`: boundaries of the research (what’s in and out of scope)  
  - `assigned_to`: team member(s) responsible for the spike  
  - `related_feature_or_goal`: what this research informs (e.g., specific feature, epic, or project goal)  
  - `sources_explored`: docs, APIs, tools, competitors, users, etc. that were consulted  
  - `findings`: summary of key insights or discoveries  
  - `recommendations`: next steps, decisions, or actions based on findings  
  - `confidence_level`: subjective confidence in the findings (e.g., High, Medium, Low)  
  - `impact_level`: how important the findings are to product direction (e.g., P1–P3)  
  - `status`: current state of the spike (e.g., Planned, In Progress, Complete)  
  - `duration`: time spent or estimated for the spike  
  - `tags`: keywords or themes (e.g., LLMs, pricing models, mobile UX)  
  - `created_by`: author of the spike  
  - `created_at`: date the spike was initiated  
  - `last_updated_by`: who last modified the spike  
  - `last_updated_at`: date of the last update  
4. Save output to `docs/research/spikes/spike_*.md`
5. Identify next steps or who to consult
```

---

### Task 1.6 – Define Solution Architecture and Standards
```markdown
🎯 POD MISSION: DevPod + ResearchPod – Define Architecture & Standards

🧾 TASK YAML:
task_id: 1.6_define_architecture_and_standards
pod: DevPod
description: Draft initial solution architecture and coding or design standards
inputs:
  - docs/project_goals.md
  - docs/features/feature_*.md
  - docs/research/spikes/spike_*.md

📁 MEMORY:
- path: docs/project_goals.md
  repo: stewmckendry/ai-delivery-framework
- path: docs/features/feature_*.md
  repo: stewmckendry/ai-delivery-framework
- path: docs/research/spikes/spike_*.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
Use GitHub File Tool to load project context + spike outputs.

Then:
# 🧠 AI-Native App Documentation Instructions

This guide outlines what to capture in your technical documentation for both the **solution architecture** and **engineering standards**. These materials should serve as living references for all team members and contributors.

---

## ✅ Part A: `solution_overview.md` — Solution Architecture

### 1. 📐 Propose a High-Level Architecture Diagram
- Visualize key components and how they interact
- Include client/server boundaries, AI services, data sources, tools, and external integrations
- Use clear labels and arrows to illustrate data flow and dependencies

### 2. 🧩 Document Major Components
For each component, include:
- `component_id`: Unique name or identifier  
- `name`: Human-readable label  
- `description`: Purpose and functionality  
- `tech_stack`: Languages, frameworks, or services used  
- `interfaces`: Key APIs, events, or contracts it exposes or consumes  
- `inputs`: Data or signals it receives  
- `outputs`: What it produces or modifies  
- `dependencies`: Other components it relies on  
- `owner`: Team or person responsible  
- `status`: (e.g., Planned, In Progress, Stable, Deprecated)

### 3. 🔄 Define System-Level Data Flow
- Describe how data flows across components  
- Call out any asynchronous patterns (e.g., queues, events)  
- Include edge cases (e.g., retries, error handling) if relevant

### 4. 🧠 Highlight AI-Specific Concerns
- `llm_usage`: What LLMs are used for (e.g., classification, reasoning, generation)  
- `memory_model`: How state is persisted (e.g., Git-based memory, vector DB)  
- `prompt_routing`: How prompts are routed to tools, functions, or models  
- `tool_invocation`: When/how tools (e.g., OpenAPI, database, retrieval) are triggered  
- `traceability`: How inputs, thoughts, and outputs are tracked across steps  
- `observability`: Logging and evaluation hooks for reasoning quality  

### 5. 🚧 Raise Architecture Gaps or Risks
- Unresolved decisions  
- Security/privacy concerns  
- Tooling or platform limitations  
- Areas flagged for future iteration

---

## ✅ Part B: `standards.md` — Project Engineering Standards

### 1. 📁 Folder and File Structure
- Define the canonical folder structure for:
  - `src/`, `data/`, `docs/`, `logs/`, `tests/`, etc.
- Include:
  - Purpose of each folder  
  - Placement of feature pods or agents  
  - Where memory, prompts, or evaluation outputs should live

### 2. 📝 File Naming Conventions
- File naming patterns by type:
  - Python: `snake_case.py`
  - Markdown: `kebab-case.md`
  - Prompt templates: `taskname_prompt.md`
- Versioning: e.g., `v1`, `v2`, date-stamped files

### 3. 💬 Prompt Format Standards
- Template structure for prompts:
  - `system`, `context`, `task_instruction`, `format_requirements`
- Naming and reuse of prompt files  
- Prompt modularity (e.g., loading from YAML or markdown)

### 4. 🪵 Logging Conventions
- Required logging for:
  - LLM calls (input, output, model used)  
  - Tool invocations (tool name, inputs, success/failure)  
  - Thought and reasoning chains  
- Log formats: JSON lines, Markdown, or structured text  
- File paths: standard naming and location in `/logs`

### 5. 🧪 Testing and Evaluation
- Unit test framework (e.g., `pytest`)  
- Test types:
  - LLM input/output assertions  
  - Tool response mocks  
  - Thought chain reproducibility  
- Evaluation standards:
  - Reasoning quality metrics  
  - Redundancy, novelty, cost-effectiveness

### 6. 🧠 AI-Specific Standards
- LLM call caching  
- Embedding deduplication  
- Trace tracking and lineage logging  
- Tool cost and call frequency monitoring

### 7. 🎨 UX & Non-Functional Standards

#### ✨ UX Standards
- Follow WCAG 2.1 AA accessibility guidelines  
- Ensure responsiveness across common screen sizes  
- Limit cognitive load (especially for AI-generated content)  
- Provide contextual help and feedback during AI-driven interactions  
- Define consistent UI patterns and component library usage  

#### ⚡️ Performance Standards
- API response time targets (e.g., < 300ms for non-AI calls)  
- Streaming or progressive loading for LLM responses  
- Caching of prompts, embeddings, or tool results where applicable  
- Limit background LLM/tool calls to reduce latency  

#### 🔒 Security & Privacy
- No PII in logs or prompts by default  
- Secure API key and model handling  
- Role-based access control if multiple user types  
- Document AI risk mitigations (e.g., hallucination guardrails)  

#### 📈 Observability & Monitoring
- Define metrics to track:
  - LLM cost per session  
  - Tool failure rate  
  - Evaluation score distributions  
- Set up alerts for spikes in failures or cost  
- Include dashboards for LLM/tool usage patterns

---

## 📌 Final Steps
- Save outputs to:
  - `docs/solution_overview.md`  
  - `docs/standards.md`
- Tag any open questions or assumptions
- Share with the team for feedback and iteration
```

---

### Task 1.7 – Feedback Summary
```markdown
🎯 POD MISSION: Human – Summarize Feedback Log

🧾 TASK YAML:
task_id: 1.7_feedback_summary
pod: Human
description: Summarize chat feedback, discussion notes, and key decisions
inputs:
  - .logs/feedback/*.md

📁 MEMORY:
- path: .logs/feedback/*.md
  repo: stewmckendry/ai-delivery-framework

📡 TOOL USE:
No tool use required.

Then:
1. Read feedback notes from the current session
2. Summarize key feedback points, open questions, and suggestions
3. Tag related task_ids or feature_ids
4. Save summary to `.logs/feedback/1.7_feedback_summary.md`
```

Let me know if you’d like test stubs created for these outputs!
