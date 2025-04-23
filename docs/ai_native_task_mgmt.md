# AI-Native Task Management Framework

This document defines a scalable, AI-native framework for managing tasks across pods, phases, and sprints in a software delivery process. It integrates seamlessly with multi-pod execution, patch promotion, GPT-based task automation, and human oversight via the DeliveryPod GPT.

---

## 🧠 Core Concepts

| Concept | Description |
|--------|-------------|
| **task_templates/** | Canonical reusable tasks by SDLC phase and step |
| **tasks.yaml** | Unified backlog with task metadata including sprint and active status |
| **.logs/** | Stores metadata such as patch history, feedback, and metrics |
| **DeliveryPod GPT** | Custom GPT agent that serves as UI to manage tasks and orchestrate project planning with human |

---

## 🧩 Multi-Pod Task Support

This framework supports **parallel task execution** across multiple pods by using `tasks.yaml` as a unified backlog:

- Each task includes metadata for sprint and active status:
  - `sprint: In-Sprint | Backlog`
  - `active: true | false`
- Pods (DevPod, QAPod, ResearchPod) work concurrently on assigned tasks
- `generate_patch_from_output.sh` uses `--task_id` to operate on the appropriate task


---

## 📁 File Structure

```bash
project_root/
├── task_templates/              # Reusable templates per phase/task
├── tasks.yaml                   # Unified project backlog + sprint + active flags
├── .patches/                    # Generated patch files
├── .logs/
│   ├── patches/                 # Metadata for each patch
│   └── feedback/                # Review/feedback records
└── chatgpt_repo/outputs/        # GPT-generated output artifacts
```

---

## 🔄 Task Lifecycle

```mermaid
graph TD
  T1[task_templates/*] --> T2[tasks.yaml]
  T2 --> G1[generate_patch_from_output.sh]
  G1 --> P1[.patches/ and .logs/patches/]
  P1 --> PR1[create_pr_from_patch.sh]
  PR1 --> D1[update tasks.yaml: done = true, updated_at]


---

## 🛠️ Human + GPT DeliveryPod Workflow

### (1) Project Initiation
- Human runs `init_project_tasks.py` to generate `tasks.yaml` from templates

### (2) Sprint Planning Ceremony
1. Human gives GPT the prompt: _"List tasks pending or to-do for sprint planning."_
2. GPT loads and filters `tasks.yaml`
3. Human selects tasks for the sprint (`sprint: In-Sprint`)
4. GPT updates and returns revised `tasks.yaml`
5. Human promotes patch if changes to tasks.yaml are confirmed

### (3) Daily Standup
1. Human asks DeliveryPod for status update
2. GPT retrieves `tasks.yaml` and shows:
   - tasks with `sprint: In-Sprint`, grouped by `active` and `pod`
3. Human selects next tasks to activate (`active: true`)
4. GPT updates tasks.yaml and returns changes for human to review and promote
5. Human requests prompt → GPT loads template from `prompts/`, validates inputs via `memory.yaml`, and returns prompt
- `task.yaml` should update when prompt is generated (start) and when patch is created (done)
- Project/sprint/active tasks must be consistent
- `memory.yaml` must update anytime outputs are finalized

---

## ✅ Automation Scripts

| Script | Role |
|--------|------|
| `init_project_tasks.py` | Seed `tasks.yaml` from `task_templates/` |
| `generate_patch_from_output.sh` | Promotes output to diff + metadata via task_id |
| `create_pr_from_patch.sh` | Applies patch, commits, pushes, and opens PR |
| `complete_task.sh` | Marks `done: true`, updates timestamp, archives in .logs |

> Sprint and activation now handled via `tasks.yaml` edits directly

## 🤝 DeliveryPod GPT as UI & Orchestrator

### Custom GPT Actions

| Endpoint | Purpose |
|----------|---------|
| `/init_tasks` | Create `tasks.yaml` from templates |
| `/plan_sprint` | Update tasks with `sprint: In-Sprint` |
| `/activate_task` | Set `active: true` for selected task |
| `/get_active_tasks` | List tasks with `active: true` |
| `/complete_task` | Set `done: true`, update timestamps |
| `/monitor_pods` | Return task state by pod and sprint |
| `/sync_memory` | Update memory.yaml from finalized task outputs |
| `/get_prompt` | Retrieve and validate prompt for task |


- Scales across **multiple pods** with 1 source of truth
- Uses **single-file task model** with sprint and activation flags
- Fully Git-compatible, patch-promotable, and GPT-aware
- Simplifies tooling while retaining powerful automation

## ✨ Next Steps

- [x] Define full GPT-human sprint and daily standup loop
- [x] Add `/sync_memory` action to support knowledge consistency
- [x] Add `/get_prompt` for task-specific standard prompt retrieval
- [ ] Implement validation to detect desync between task files and memory.yaml
- [ ] Add CLI or dashboard for task selection and flow visibility


