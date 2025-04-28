# 🧠 AI Memory in Delivery: Supporting an AI-Native Development Lifecycle

---

## Core Operating System

The AI-native delivery model revolves around four key components:

| Component         | Purpose                                                             |
|-------------------|---------------------------------------------------------------------|
| `task.yaml`        | Prescribes all work: task IDs, inputs, outputs, status, assigned pod |
| `memory.yaml`      | Tracks file existence, meaning, and users                           |
| `prompts/`         | Stores reusable prompt templates for tasks                          |
| Human-in-the-loop  | Provides ideas, vision, feedback, and approval before patch promotion |

Synced via:

- File conventions (e.g., `.logs/feedback/<task_id>.md`)
- Automation scripts (e.g., `scripts/link_feedback.py`)
- Standardized prompt templates (e.g., `prompts/dev/implement_feature.txt`)

---

### 🧠 Note on DevPod

**DevPod** is a cross-functional pod: product thinkers, analysts, and developers collaborate to spec, assess, and build features end-to-end.

---

### ✅ Definition of Ready (DoR)

A task is "Ready" when:

- Defined in `task.yaml` with `description`, `inputs`, `outputs`, `pod_owner`, `prompt`, and optionally `feedback_file`
- All inputs are in Git and indexed in `memory.yaml`
- Success criteria are clear (e.g., acceptance criteria or embedded prompts)
- `ready: true` flag is optionally set

**Stored in:**
- `task.yaml`
- Checklist: `docs/workflows/definition_of_ready.md`
- Validated via: `scripts/validate_ready.py`

---

### ✅ Definition of Done (DoD)

A task is "Done" when:

- All outputs are present in Git
- `memory.yaml` is updated
- Tests are written and passing
- Feedback captured in `.logs/feedback/`
- Task status updated to `done`

**Stored in:**
- `task.yaml`
- Checklist: `docs/workflows/definition_of_done.md`
- Validated via: `scripts/validate_done.py`

---

# 🚀 Delivery Phases

---

## Phase 1: Discovery

### Purpose
Define what the app is, who it serves, and how it will be built.

### Key Pods
- DevPod
- QAPod
- ResearchPod
- WoWPod
- Human

### Core Tasks

| Task | Owner | Outputs |
|-----|------|---------|
| 1.1 Capture project goals | Human + DevPod | `docs/project_goals.md`, update `memory.yaml[project_goals]` |
| 1.2 Define user & delivery flows | DevPod, WoWPod | `docs/personas/*.md`, `docs/journeys/*.md`, `docs/workflows/delivery_flow.md` |
| 1.3 Break work into features | Human + DevPod | `docs/features/feature_x.md`, update `memory.yaml[features]` |
| 1.4 Write acceptance criteria | Human + QAPod | `docs/qa/acceptance_matrix.md`, updated features |
| 1.5 Research open questions | ResearchPod | `docs/research/spikes/*.md`, update `memory.yaml[research_spikes]` |
| 1.6 Define solution architecture | DevPod + ResearchPod | `docs/architecture/solution_overview.md` |
| 1.7 Summarize feedback | Human | `.logs/feedback/<task_id>.md`, linked in `task.yaml` |

---

## Phase 2: Iterative Development

### Purpose
Deliver features rapidly and reliably via parallel Pod workflows.

### Key Pods
- DevPod
- QAPod
- ResearchPod
- WoWPod
- DeliveryPod
- Human

### Core Tasks

| Task | Owner | Outputs |
|-----|------|---------|
| 2.0 Draft deployment guide | DevPod + DeliveryPod | `docs/release/deployment_book.md` |
| 2.1 Assign and prompt tasks | Human | `task.yaml`, prompts |
| 2.2 Create patches & assess impact | DevPod | `.patches/*.diff`, updated memory |
| 2.3 Review and test patches | QAPod | `tests/`, `docs/qa/` |
| 2.4 Resolve unknowns | ResearchPod | `docs/research/answers/*.md` |
| 2.5 Review outputs | Human | `.logs/feedback/<task_id>.md` |
| 2.6 Promote patch | DeliveryPod | Feature branch updates |
| 2.7 Agile rituals | WoWPod | `.logs/rituals/`, `docs/workflows/` |
| 2.8 Track delivery metrics | DeliveryPod | `docs/metrics/` |

---

## Phase 3: End-to-End Testing

### Purpose
Validate full system functionality across user flows and edge cases.

### Key Pods
- QAPod
- DevPod
- WoWPod
- DeliveryPod
- Human

### Core Tasks

| Task | Owner | Outputs |
|-----|------|---------|
| 3.1 Define E2E test plan | QAPod | `docs/qa/e2e_test_plan.md` |
| 3.2 Execute E2E tests | QAPod | `.logs/tests/e2e_results.md`, bug tasks |
| 3.3 Fix bugs | DevPod | Bug patches |
| 3.4 E2E demos | WoWPod | `docs/rituals/e2e_walkthrough.md` |
| 3.5 Track issues & metrics | DeliveryPod | `docs/metrics/e2e_summary.md` |

---

## Phase 4: Cutover & Go Live

### Purpose
Finalize production readiness and stabilize the release.

### Key Pods
- WoWPod
- DeliveryPod
- DevPod
- QAPod
- Human

### Core Tasks

| Task | Owner | Outputs |
|-----|------|---------|
| 4.1 Create cutover plan | DeliveryPod | `docs/workflows/cutover_plan.md` |
| 4.2 Run final smoke tests | QAPod | `.logs/tests/smoke_test_results.md` |
| 4.3 Deploy go-live build | DevPod | Release tag, `.logs/release/release_notes.md` |
| 4.4 Communicate release | Human | `docs/release/launch_announcement.md` |
| 4.5 Run go-live retro | WoWPod | `docs/rituals/go_live_retrospective.md` |
| 4.6 Write run book | DevPod + WoWPod | `docs/release/run_book.md` |
| 4.7 Finalize deployment book | DevPod | `docs/release/deployment_book.md` |

---

# 🛠️ Technical Specification

---

## 📁 Core Project Structure

```
project-root/
├── task.yaml
├── memory.yaml
├── prompts/
├── docs/
├── src/
├── test/
├── .logs/
├── .patches/
└── scripts/
```

---

## 🧠 Core YAML Files

### `task.yaml`
```yaml
tasks:
  task_id:
    description: "Task description"
    pod_owner: DevPod
    status: pending
    prompt: prompts/dev/implement_feature.txt
    inputs:
      - docs/features/feature_summary.md
    outputs:
      - src/features/summary.py
    feedback_file: .logs/feedback/feature_summary.md
    ready: true
    done: false
```

### `memory.yaml`
```yaml
features:
  - path: docs/features/feature_summary.md
    tags: [summary, MVP, DevPod]
    related_tasks: [feature_summary]
    updated_at: 2025-04-20
```

---

## ⚙️ Core Automation Scripts

- `scripts/link_feedback.py`
- `scripts/validate_ready.py`
- `scripts/validate_done.py`
- `scripts/generate_patch.py`
- `scripts/add_task.py`
- `scripts/update_memory.py`
- `scripts/sync_task_memory.py`
- `scripts/load_prompt.py`
- `scripts/load_input_urls.py`

---

## 📜 Markdown Templates

- `docs/workflows/definition_of_ready.md`
- `docs/workflows/definition_of_done.md`
- `docs/qa/e2e_test_plan.md`
- `docs/release/deployment_book.md`
- `docs/release/run_book.md`
- `docs/rituals/go_live_retrospective.md`
- `docs/release/launch_announcement.md`

---

## 📊 Metrics

- `docs/metrics/weekly_summary.md`
- `docs/metrics/e2e_summary.md`
- Computed from `task.yaml`, `.logs/`, and `memory.yaml`

---

## 🔄 Visual: Pod Interactions

```
  Human
    │     ┌────────────┐
    └────▶│   DevPod    │────┐
          └────┬───────┘    │
               │            ▼
          ┌────▼─────┐  ┌─────────┐
          │  QAPod   │  │Research│
          └────┬─────┘  └──┬──────┘
               │          │
               ▼          ▼
         .logs/, task.yaml, memory.yaml
               │          ▲
         ┌─────▼────┐     │
         │Delivery  │◀────┘
         │  Pod     │
         └────┬─────┘
              ▼
          GitHub PR
```

---

# 🎉 AI-Native Delivery System Complete

You now have a fully operational, pod-based, memory-driven, AI-native software development lifecycle ready to deliver robust features at scale.