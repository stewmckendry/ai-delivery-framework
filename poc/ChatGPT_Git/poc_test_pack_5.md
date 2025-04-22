# 🧪 PoC Test Pack – Discovery Tasks 1.5 to 1.7

This test pack supports proof-of-concept runs for Tasks 1.5, 1.6, and 1.7 using the AI-native delivery framework with GitHub memory and custom GPT tooling.

---

## ✅ Objectives by Task

### 🧾 Task 1.5 – Research Spikes or Open Questions
**Goal:** Investigate unknowns or risks raised during Discovery. Document research findings and recommendations.

**Files:**
- `docs/project_goals.md`
- `docs/features/feature_*.md`

**Expected Output:**
- Markdown files under `docs/research/spikes/spike_*.md`

**Prompt Template:**
- `prompts/research/research_spikes.txt`

---

### 🧾 Task 1.6 – Define Solution Architecture and Standards
**Goal:** Propose technical architecture and shared standards to guide future delivery.

**Files:**
- `docs/project_goals.md`
- `docs/features/feature_*.md`
- `docs/research/spikes/spike_*.md`

**Expected Output:**
- `docs/architecture/solution_overview.md`
- `docs/architecture/standards.md`

**Prompt Template:**
- `prompts/dev/define_architecture.txt`

---

### 🧾 Task 1.7 – Feedback Summary
**Goal:** Summarize feedback and decisions from previous work sessions.

**Files:**
- `.logs/feedback/*.md`

**Expected Output:**
- `.logs/feedback/1.7_feedback_summary.md`

**Prompt Template:**
- `prompts/human/summarize_feedback.txt`

---

## 🔁 Workflow
1. Run the relevant prompt in a GPT session (ResearchPod, DevPod, or Human)
2. Load required files using GitHub tool
3. Let GPT complete and propose output content
4. Save outputs to the repo (or create patch)
5. Log feedback and update task.yaml status

---

## 📁 Supporting File Checklist
Ensure the following exist:
- `docs/project_goals.md`
- `docs/features/feature_*.md`
- `.logs/feedback/` directory (even if empty)

Post-output:
- `docs/research/spikes/spike_*.md`
- `docs/architecture/solution_overview.md`
- `docs/architecture/standards.md`
- `.logs/feedback/1.7_feedback_summary.md`

---

Let me know if you’d like to auto-generate data stubs for the spike, architecture, or feedback files!


# 📁 Data Stubs – Supporting Files for Tasks 1.5 to 1.7

These markdown stubs provide minimal content to support PoC testing of Discovery Tasks 1.5 through 1.7.

---

## 📄 docs/research/spikes/spike_sample.md
```markdown
# Spike: Compare GitHub Tool Retrieval Approaches

## Question
How should GPT retrieve multiple files from GitHub in a reliable, scalable way?

## Related Features
- Guided file-based memory lookup

## Method
- Compared raw URL fetch vs. OpenAPI tool
- Tested batch-fetching performance and failure behavior

## Findings
- GPT UI fails to reliably handle raw URLs
- OpenAPI + batch endpoint is stable

## Recommendation
Adopt GitHub proxy tool with `/batch-files` route

## Status
Resolved
```

---

## 📄 docs/architecture/solution_overview.md
```markdown
# Solution Architecture Overview

This architecture supports AI-native delivery using GPT pods, Git memory, and tooling APIs.

## Components
- Custom GPTs for each pod
- GitHub + OpenAPI tool for file memory
- FastAPI patch + log promotion system

## Flow
1. Human assigns task
2. GPT fetches memory, runs reasoning
3. Outputs saved or proposed as patches
```

---

## 📄 docs/architecture/standards.md
```markdown
# Project Standards

## Code Organization
- Use `src/`, `docs/`, `.logs/`, `prompts/`, `tests/`

## Prompt Format
- PoC-style: task_id, pod, inputs, memory, tool use, reasoning steps

## Logging
- Feedback, metrics, thought traces stored in `.logs/`

## File Naming
- Features: `feature_<slug>.md`
- Spikes: `spike_<topic>.md`
- Logs: `feedback/<task_id>.md`, `metrics.yaml`
```

---

## 📄 .logs/feedback/1.7_feedback_summary.md
```markdown
# Feedback Summary – Discovery Phase

## What Worked
- Memory file retrieval using GitHub tool
- Metadata-driven prompts and outputs

## Open Questions
- When should patches be auto-promoted?
- How can we surface stale memory entries?

## Decisions
- Move forward with standard task.yaml + memory.yaml
- Prioritize Phase 2 scaffolding next
```

Let me know when you're ready to run this PoC or scaffold the next phase!