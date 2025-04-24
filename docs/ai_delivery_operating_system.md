# AI Memory in Delivery: Supporting an AI-Native Development Lifecycle

## 🧠 Core Operating System

The AI-native delivery system is built around four foundational components:

| Component         | Purpose                                                                 |
|------------------|-------------------------------------------------------------------------|
| `task.yaml`      | Prescribes all work: task IDs, inputs, outputs, status, assigned pod    |
| `memory.yaml`    | Tracks what files exist, what they mean, who uses them                  |
| `prompts/`       | Stores prompt templates for initiating or completing pod tasks          |
| Human-in-the-loop| Provides ideas, vision, feedback and approval before patch promotion    |

These are synced via:
- File conventions (e.g., `.logs/feedback/<task_id>.md`)
- Automated scripts (e.g., `scripts/link_feedback.py` to associate feedback with tasks)
- Standard prompt storage (e.g., `prompts/dev/implement_feature.txt`)

### Note on DevPod
In this system, **DevPod** is a cross-functional product pod. It includes product thinkers, analysts, and developers who co-create feature specs with the human lead, assess technical implications, and build features end-to-end.

### ✅ Definition of Ready (DoR)
A task is considered "Ready" when:
- It is defined in `task.yaml` with required fields: `description`, `inputs`, `outputs`, `pod_owner`, `prompt`, and optionally `feedback_file`
- All inputs are available in Git and indexed in `memory.yaml`
- There is a clear understanding of success criteria (e.g., embedded A/Cs or prompt)
- Optionally includes `ready: true` to flag readiness

**Stored in:**
- `task.yaml` per task
- Optional checklist in `docs/workflows/definition_of_ready.md`
- Can be validated by script (e.g., `scripts/validate_ready.py`)

### ✅ Definition of Done (DoD)
A task is considered "Done" when:
- All outputs listed in `task.yaml` are present in the repo
- `memory.yaml` is updated with all relevant artifacts
- Associated tests are written and passing
- Feedback has been captured in `.logs/feedback/`
- Task includes `done: true` or status is marked as `done`

**Stored in:**
- `task.yaml` per task
- Checklist in `docs/workflows/definition_of_done.md`
- Can be validated by script (e.g., `scripts/validate_done.py`)

These guardrails ensure shared expectations, improve automation, and reduce rework — especially with multiple pods working in parallel.


## Phase 1: Discovery

### Purpose
Define what the app is, who it serves, and how it will be built — including the user flow, delivery flow, solution architecture, and supporting research.

### Key Pods Involved
- DevPod (product, analysts, devs)
- QAPod (writing acceptance criteria)
- ResearchPod (tooling, standards)
- WoWPod (workflows, architecture)
- Human (vision, feedback)

### Tasks & Memory Actions

#### 1.1 Capture project goals (Owner: Human + DevPod)
- Input: `docs/project_goals.md`
- Output: updated memory.yaml under `project_goals`
- Retrieval: File path lookup

#### 1.2 Define user flows and delivery flows (Owner: Human + DevPod for user flows, WoWPod for delivery flows)
- **User Flow**: personas, end-to-end app experience
  - Outputs: `docs/personas/*.md`, `docs/journeys/*.md`
  - Memory: `memory.yaml[user_flows]`
- **Delivery Flow**: SDLC, pod roles, release phases
  - Outputs: `docs/workflows/delivery_flow.md`
  - Memory: `memory.yaml[delivery_flow]`

#### 1.3 Break work into features or hypotheses (Owner: Human + DevPod)
- Outputs: `docs/features/feature_x.md`
- Memory: `memory.yaml[features]`

#### 1.4 Write acceptance criteria (Owner: Human, with QAPod support)
- Inputs: feature specs
- Outputs: `docs/qa/acceptance_matrix.md`, updated feature files
- Memory: `memory.yaml[qa_refs]`

#### 1.5 Research spikes or open questions (Owner: ResearchPod)
- Outputs: `docs/research/spikes/*.md`
- Memory: `memory.yaml[research_spikes]`

#### 1.6 Define solution architecture and standards (Owner: DevPod + ResearchPod)
- Outputs: `docs/architecture/solution_overview.md`, `standards.md`
- Memory: `memory.yaml[architecture]`

#### 1.7 Feedback summary (Owner: Human)
- Written to: `.logs/feedback/<task_id>.md`
- Linked via: `task.yaml[feedback_file]`
- Created by: asking ChatGPT to summarize chat at end of session



## Phase 2: Iterative Development

### Purpose
Deliver features rapidly and reliably using parallel pod workflows — DevPod writes code, QAPod tests, ResearchPod resolves unknowns, and the human-in-the-loop reviews outputs before anything lands in Git.

### Key Pods Involved
- DevPod (1+ per feature, cross-functional)
- QAPod
- ResearchPod
- WoWPod (rituals and process improvements)
- DeliveryPod (metrics and issue tracking)
- Human (task assignment, vision, review)

### Tasks & Memory Actions

#### 2.0 Start deployment guide (Owner: DevPod, supported by DeliveryPod)
- Inputs:
  - Early deployment patterns, build scripts, environment configs
- Outputs:
  - Initial `docs/release/deployment_book.md`
  - Local and staging deploy instructions
  - Linked in `memory.yaml[deployment_book]`

#### 2.1 Assign task and prompt DevPod (Owner: Human)
- Task defined in `task.yaml`
- Feature spec (`docs/features/feature_summary.md`) defines functionality and may contain embedded acceptance criteria
- The initial feature spec (including A/Cs) is typically authored by the human lead (acting as product owner)
- DevPod may update the spec post-implementation with tech details, edge cases, known limitations, and rationale

#### 2.2 DevPod generates patch and assesses impact (Owner: DevPod)
- DevPod:
  - Creates/modifies files in `src/`, `docs/`, `scripts/`
  - Evaluates impact to existing code (e.g., identify refactors, affected modules)
- Memory used:
  - `memory.yaml[features]` → related modules, specs
  - Git-based search → find files with matching functions, imports, or references
- Inputs/outputs updated to reflect any changes to existing files
- Patch is stored as `.patches/*.diff`

#### 2.3 QAPod reviews patch and writes tests (Owner: QAPod)
- Inputs:
  - DevPod's patch or updated files
  - Feature spec (including embedded or linked acceptance criteria)
- Outputs:
  - `tests/` files
  - QA logs or checklists in `docs/qa/`

#### 2.4 ResearchPod assists with unknowns (Owner: ResearchPod)
- Tasked via `task.yaml` with resolving open questions
- Outputs:
  - `docs/research/answers/*.md`
  - Updates `memory.yaml[research_answers]`

#### 2.5 Human-in-the-loop reviews all outputs (Owner: Human)
- Reviews DevPod patch, QAPod coverage, and ResearchPod findings
- Approves or requests changes
- Feedback saved to `.logs/feedback/<task_id>.md`, linked via `task.yaml`

#### 2.6 Promote patch to feature branch (Owner: DeliveryPod)
- GitHub Action (or script) runs `generate_patch.py`
- Patch is promoted to a feature branch

#### 2.7 WoWPod runs agile rituals (Owner: WoWPod)
- Facilitates sprint planning, standups, and retrospectives
- Ritual outputs stored in `docs/workflows/` or `.logs/rituals/`

#### 2.8 DeliveryPod reviews metrics (Owner: DeliveryPod)
- Tracks velocity, quality, issues/risks, decisions
- Outputs weekly summaries and updates memory

---

### Memory Models Used
- **Primary**: `memory.yaml` and Git search
- **Optional Enhancements**:
  - Vector DB for semantically similar code/docs (used by QAPod or ResearchPod)
  - Metadata filtering for role-specific retrieval

---

### Outputs
- `src/` code
- `tests/` validation
- `docs/features/`, `docs/qa/`, `docs/metrics/`
- `memory.yaml`, `task.yaml`, `prompts/`, `.logs/feedback/`, `.logs/rituals/`
- Initial draft of `docs/release/deployment_book.md`


## Phase 3: End-to-End Testing

### Purpose
Validate that the full application — or major slices of functionality — work together as expected across user flows, edge cases, and environments.

### Key Pods Involved
- QAPod (test design and execution)
- DevPod (bug fixing, instrumentation)
- WoWPod (coordinating dry runs and feedback loops)
- DeliveryPod (tracking issues, quality metrics)
- Human (orchestrates E2E scope, approves readiness)

### Tasks & Memory Actions

#### 3.1 Define E2E test plan (Owner: QAPod)
- Inputs:
  - Feature specs and user flows (`docs/features/`, `docs/journeys/`)
  - Acceptance matrix from earlier phases
- Outputs:
  - `docs/qa/e2e_test_plan.md`
  - Structured checklist or scenario list in `test/e2e/`

#### 3.2 Execute E2E scenarios (Owner: QAPod)
- Inputs:
  - Integrated app (locally or in staging)
  - E2E test cases
- Outputs:
  - Test logs and result summaries (`.logs/tests/e2e_results.md`)
  - Bugs filed to `task.yaml` with new IDs
  - Updates to memory.yaml if issues affect known modules

#### 3.3 Fix bugs and update implementation (Owner: DevPod)
- Inputs:
  - QA logs, bug reports, failing E2E scenarios
- Outputs:
  - Patch files with fixes
  - Updates to impacted tests or docs

#### 3.4 Coordinate E2E review or demo (Owner: WoWPod)
- Outputs:
  - Demo script or dry-run notes (`docs/rituals/e2e_walkthrough.md`)
  - Optional recordings or markdown recap

#### 3.5 Track issues and finalize quality metrics (Owner: DeliveryPod)
- Inputs:
  - Test results, bug history, task.yaml status fields
- Outputs:
  - Metrics dashboard in `docs/metrics/e2e_summary.md`
  - Final update to memory.yaml for all test coverage and known edge cases

---

### Outputs
- `docs/qa/e2e_test_plan.md`
- `test/e2e/` test cases
- `.logs/tests/e2e_results.md`
- Bug patches and logs
- `docs/metrics/e2e_summary.md`
- `memory.yaml`, `task.yaml`, updated source/tests/docs


## Phase 4: Cutover & Go Live

### Purpose
Ensure the app is ready for production use and that all final activities (handoffs, documentation, stakeholder communication, and confidence checks) are completed smoothly.

### Key Pods Involved
- WoWPod (facilitates release planning and team readiness)
- DeliveryPod (coordinates cutover plan, monitors rollout)
- DevPod (final fixes, deployment support)
- QAPod (final verification, smoke testing)
- Human (final sign-off, stakeholder comms)

### Tasks & Memory Actions

#### 4.1 Create cutover checklist and plan (Owner: DeliveryPod)
- Inputs:
  - Completed `task.yaml`
  - Final test and metrics summaries
- Outputs:
  - `docs/workflows/cutover_plan.md`
  - Linked in `memory.yaml[cutover_plan]`

#### 4.2 Run final smoke tests in production (Owner: QAPod)
- Inputs:
  - Cutover checklist
  - Production environment
- Outputs:
  - `.logs/tests/smoke_test_results.md`
  - Updated task or bug entries if issues found

#### 4.3 Execute go live deployment (Owner: DevPod)
- Inputs:
  - Deployment scripts and build artifacts
  - Readiness signals from all pods
- Outputs:
  - Release tag, changelog update
  - Confirmation in `.logs/release/release_notes.md`

#### 4.4 Communicate release and transition ownership (Owner: Human)
- Outputs:
  - `docs/release/launch_announcement.md`
  - Handoff instructions or user documentation (if needed)
  - Final update to memory.yaml with live URLs and contact info

#### 4.5 Facilitate go-live retrospective and stabilize (Owner: WoWPod)
- Inputs:
  - Team feedback, post-release metrics
- Outputs:
  - `docs/rituals/go_live_retrospective.md`
  - Action items assigned to future tasks

#### 4.6 Create run book (Owner: DevPod, supported by WoWPod + DeliveryPod)
- Inputs:
  - System architecture, deployment scripts, known issues, feedback logs
- Outputs:
  - `docs/release/run_book.md`
  - Includes sections on operations, monitoring, known issues, escalation steps
  - Linked in `memory.yaml[run_book]`

#### 4.7 Create deployment book (Owner: DevPod, supported by DeliveryPod)
- Inputs:
  - Deployment scripts, environment configs, system diagram
- Outputs:
  - `docs/release/deployment_book.md`
  - Includes build, deploy, verify instructions for local, staging, and prod
  - Linked in `memory.yaml[deployment_book]`

---

### Outputs
- `docs/release/deployment_book.md`
- `docs/release/run_book.md`
- `docs/workflows/cutover_plan.md`
- `.logs/tests/smoke_test_results.md`
- `docs/release/launch_announcement.md`
- `.logs/release/release_notes.md`
- `docs/rituals/go_live_retrospective.md`
- Final updates to `memory.yaml`, `task.yaml`

✅ At this point, the app is live, memory is frozen for the release, and all delivery artifacts are traceable in Git.

---

🎉 **AI-Native Delivery System Complete**
You’ve now mapped all phases of building and shipping with pods — Discovery, Iterative Development, End-to-End Testing, and Go Live — each powered by task-driven memory, prompts, automation, and human-in-the-loop collaboration.

---

## 📐 Technical Specification for Implementation

This section outlines everything a ChatGPT DevPod needs to implement the AI-native delivery operating system — from foundational structure to runtime automation.

### 📁 Core Project Structure
```
project-root/
├── task.yaml                      # Task-level delivery plan
├── memory.yaml                    # File index with tags, roles, purpose
├── prompts/                       # Reusable system + task prompts
│   ├── dev/implement_feature.txt
│   ├── qa/write_tests.txt
│   └── delivery/metrics_summary.txt
├── docs/
│   ├── features/
│   ├── qa/
│   ├── workflows/
│   ├── architecture/
│   └── release/
├── src/                           # Application source code
├── test/                          # Tests (unit + E2E)
│   └── e2e/
├── .logs/
│   ├── feedback/
│   ├── release/
│   ├── rituals/
│   └── tests/
├── .patches/                      # ChatGPT-generated diffs
└── scripts/                       # Automation helpers
```

### 🧠 Core YAML Files
- `task.yaml`: every task's ID, pod, prompt path, inputs/outputs, status
- `memory.yaml`: tracks key files and knowledge references with tags
  ```yaml
  features:
    - path: docs/features/feature_summary.md
      tags: [summary, MVP, DevPod]
  prompts:
    - path: prompts/dev/implement_feature.txt
      tags: [DevPod, generate_patch]
  ```

### ⚙️ Automation Scripts
- `scripts/link_feedback.py`: auto-links feedback markdown to `task.yaml`
- `scripts/validate_ready.py`: checks Definition of Ready conditions
- `scripts/validate_done.py`: ensures DoD completion for each task
- `generate_patch.py`: builds ChatGPT patch into `.diff`

### 📄 Templates (Markdown)
- `docs/workflows/definition_of_ready.md`
- `docs/workflows/definition_of_done.md`
- `docs/release/run_book.md`
- `docs/release/deployment_book.md`
- `docs/release/launch_announcement.md`

### 📊 Metrics and Dashboards
- `docs/metrics/weekly_summary.md`
- `docs/metrics/e2e_summary.md`
- DeliveryPod queries `task.yaml`, `.logs/`, and `memory.yaml` to compute:
  - Velocity (tasks/week)
  - Quality (bugs, test coverage)
  - Trace (decisions, feedback captured)

### 🔄 Pod Interactions (Visual)
```text
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

### 🧾 Metadata Models for YAML Files

#### `task.yaml`
```yaml
tasks:
  task_id:
    description: "Short description of the task"
    pod_owner: DevPod | QAPod | ResearchPod | DeliveryPod | WoWPod
    status: pending | in_progress | done
    prompt: prompts/dev/implement_feature.txt
    inputs:
      - docs/features/feature_summary.md
    outputs:
      - src/features/summary.py
    feedback_file: .logs/feedback/feature_summary.md
    ready: true  # optional flag for DoR compliance
    done: false  # updated by validation scripts
    created_by: human
    created_at: 2025-04-20T10:00:00
    updated_at: 2025-04-21T12:34:56
```

#### `memory.yaml`
```yaml
features:
  - path: docs/features/feature_summary.md
    tags: [summary, MVP, DevPod]
    related_tasks: [feature_summary]
    updated_at: 2025-04-20

prompts:
  - path: prompts/dev/implement_feature.txt
    tags: [DevPod, patch]
    description: "Prompt for implementing a new feature"

qa_refs:
  - path: docs/qa/acceptance_matrix.md
    tags: [acceptance, QAPod]

cutover_plan:
  - path: docs/workflows/cutover_plan.md
    tags: [release, DeliveryPod]
```

### 🧰 Template Guidance
- **Every input and output** should be matched with a markdown template (or prompt) for consistency
- Examples:
  - `docs/features/feature_x.md` → feature template
  - `docs/research/spikes/question_y.md` → spike template
  - `docs/qa/e2e_test_plan.md` → test plan template

### 🤖 Automation Opportunities
Suggested additional scripts:
- `scripts/add_task.py`: create new task entry in `task.yaml`
- `scripts/update_memory.py`: append/modify `memory.yaml` entries
- `scripts/sync_task_memory.py`: ensure outputs in `task.yaml` match entries in `memory.yaml`
- `scripts/load_prompt.py`: resolve prompt path and print for use in ChatGPT UI
- `scripts/load_input_urls.py`: extract and print clickable GitHub URLs for all task inputs

These will reduce manual effort and ensure pods stay in sync with Git-tracked memory.

---

🚀 Next Steps for Implementation

Here are the recommended actions to fully activate and scale the AI-native delivery system:

📁 File & Template Setup
- Scaffold task.yaml with starter Phase 1 tasks
- Create an initial memory.yaml with tagged references
- Add markdown templates to docs/ for:
  - Feature specs (docs/features/)
  - QA acceptance criteria (docs/qa/)
  - E2E test plans (docs/qa/e2e_test_plan.md)
  - Cutover plan (docs/workflows/cutover_plan.md)
  - Go-live retrospective (docs/rituals/go_live_retrospective.md)
  - Run book (docs/release/run_book.md)
  - Deployment book (docs/release/deployment_book.md)
  - Launch announcement (docs/release/launch_announcement.md)
🧠 Prompt + Script Integration 
- Populate prompts/ with system and pod-specific prompts
- Build scripts to:
  - add_task.py: create new task entries
  - update_memory.py: maintain memory.yaml entries
  - sync_task_memory.py: ensure tasks and memory align
  - link_feedback.py: connect logs to task.yaml
  - load_prompt.py: preview or load prompt contents
  - load_input_urls.py: get clickable GitHub links from task inputs
  - validate_ready.py: check DoR compliance
  - validate_done.py: check DoD compliance
🔁 GitHub + Patch Pipeline
- Finalize generate_patch.py logic for outputting .diff
- Connect GitHub Action to auto-promote patches and open PRs
- Test PR-based patch delivery loop (task → patch → PR)
🧪 Pilot + Iterate
- Apply the operating system to a live project (e.g., Concussion AgentForms)
- Run Phase 1 tasks with DevPod and Human in the loop
- Test workflows from memory lookup to prompt to patch to GitHub
- Conduct a go-live retro on the memory system itself and refine