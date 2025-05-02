# 🧠 System Overview

The AI-Native Delivery Framework is composed of modular, interoperable systems designed to enable continuous improvement.

---

## 1. User View

| Actor | Role |
|:---|:---|
| Human Lead | Guides task activation, reviews reasoning, approves patches |
| GPT Pods | Specialized agents completing tasks with structured reasoning |
| Reviewers | Optional humans validating major patches or outputs |

Pods work semi-autonomously, with Human Leads acting as quality guardians and flow enablers.

---

## 2. Process View

1. Task is created or activated.
2. Pod pulls prior related memory and task metadata.
3. Pod generates outputs + reasoning traces.
4. Outputs promoted via automated patching system.
5. Metrics and memory updated.

Handoff notes ensure Pods leave "breadcrumbs" for continuity.

---

## 3. Data & AI View

- **Memory.yaml** indexes project knowledge.
- **Reasoning Traces** stored per task for later analysis.
- **Patch Metadata** (e.g., summary, outputs, changes) stored per patch.
- **Metrics** generated from task progression and thought quality.
- **Searchable Memory** enables Pods to "think in context" before generating.

---

## 4. Technology Stack View

| Component | Stack |
|:---|:---|
| API Server | FastAPI (hosted, public/private options) |
| Repo Management | GitHub + PyGitHub |
| Memory Search | JSON + (optional) Embeddings |
| Prompt Hosting | GitHub Pages, local file serving |
| Automation | Custom GPT Actions linked to API |

---

## 5. System Behavior in Practice

- Memory grows organically.
- Reasoning improves patch-by-patch.
- Human Leads manage delivery **by guiding context**, not micromanaging actions.
- System metrics illuminate not just "what got done," but *how thoughtfully it was done*.

---

## 6. Example Project Flow

1. Initiate project with a seed task list.
2. Pods pick up tasks, generate reasoning + outputs.
3. Outputs bundled into patches, reviewed, merged.
4. Metrics analyzed to improve reasoning quality over time.
5. Framework learns, scales, and compounds knowledge.

---
