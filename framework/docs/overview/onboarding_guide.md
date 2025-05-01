# 🧭 Human Lead Onboarding Guide

Welcome to the AI-Native Delivery System! This guide is your reference for how the system works, how to run tasks, and how to guide GPT Pods through structured, traceable delivery.

---

## 📌 1. System Overview

This system enables AI-assisted, task-based software delivery using:

- **YAML-based memory and task tracking**
- **Structured reasoning capture (`reasoning_trace.yaml`)**
- **OpenAPI-driven GPT tooling**
- **Git versioning + changelog auditing**
- **Pod workflows (DevPod, QAPod, ProductPod, etc.)**

---

## 📁 2. Repo Structure

| Folder | Purpose |
|--------|---------|
| `project/task.yaml` | Prescribes all tasks: inputs, owners, status |
| `project/memory.yaml` | Tracks meaningful files + metadata |
| `project/outputs/<task_id>/` | Logs for each task (chain of thought, outputs, reasoning) |
| `project/.logs/` | Changelogs and rollback logs |
| `project/docs/` | Project documentation (like this guide!) |

---

## 👥 Meet the AI Pods

This system is structured around modular, role-based AI Pods that mirror real-world delivery teams:

| **Pod** | **Mission** | **Core Capabilities** |
|---------|-------------|------------------------|
| **ProductPod** | Design, build, and evolve features and systems | Requirements, solutioning, building, patching |
| **QAPod** | Ensure quality and readiness across outputs | Test planning, validation, issue detection, acceptance checking |
| **ResearchPod** | Explore external knowledge to guide solutions | Research, summarize insights, recommend options |
| **WoWPod** | Define and improve how Pods and system work | Process design, standards, retrospectives, rituals |
| **DeliveryPod** | Manage task flow, metrics, retrospectives | Task tracking, metrics generation, reporting |
| **WriterPod** | Communicate work internally and externally | Documentation, blogs, changelogs, release notes |
| **PromptPod** | Design and optimize prompts for GPTs | Draft, refine, and enhance prompts for better task execution |

---

## 🧱 What Types of Tasks Do We Have?

Tasks are structured around an app delivery lifecycle, but the framework can be adapted to any AI-native delivery use case.

### Phase 1: Discovery
- `1.1_capture_project_goals`
- `1.2_define_user_and_delivery_flows`
- `1.3_break_into_features`
- `1.4_write_acceptance_criteria`
- `1.5_research_spikes`
- `1.6_define_architecture_and_standards`

### Phase 2: Iterative Development
- `2.1_design_feature_and_tech_spec`
- `2.2_build_and_patch`
- `2.3_qa_review_feature`
- `2.4a_fix_bugs_from_qa`
- `2.4b_retest_after_fixes`
- `2.5_research_assist`
- `2.7_agile_metrics`
- `2.8_prepare_deployment_guide`

### Phase 3: E2E Testing
- `3.1_define_e2e_test_plan`
- `3.2_execute_e2e_scenarios`
- `3.3_fix_bugs_e2e`
- `3.4_coordinate_e2e_demo`
- `3.5_finalize_quality_metrics`

### Phase 4: Go Live
- `4.1_create_cutover_plan`
- `4.2_final_smoke_tests`
- `4.3_go_live_deployment`
- `4.4_announce_go_live`
- `4.5_go_live_retro`

---

## 🔄 Task Lifecycle

| Phase | Tool | Description |
|-------|------|-------------|
| Start Task | `/tasks/start` | Marks task in progress, returns prompt, inputs, handoff |
| Log Thoughts | `/tasks/append_chain_of_thought` | Appends structured reasoning |
| Complete Task | `/tasks/complete` | Submits outputs, reasoning trace, handoff note |
| Reopen Task | `/tasks/reopen` | Reopens task and logs reasoning why |

---

## ⚙️ Key GPT Tools

These tools are available to the GPT Pods (and you) for completing, organizing, and reviewing work. They follow OpenAPI definitions and are callable via the system interface.

| Tool | Use |
|------|-----|
| `/tasks/update_metadata` | Update task fields like description, inputs, and outputs |
| `/tasks/activate` | Mark one or more tasks as ready or in-progress |
| `/tasks/clone` | Duplicate an existing task (with optional changes) |
| `/tasks/create` | Create a brand-new task from scratch |
| `/tasks/getTaskDetails` | Retrieve full metadata for a task |
| `/tasks/next` | Retrieve the next recommended task based on plan |
| `/tasks/commit_and_log_output` | Commit output files mid-task with changelog |
| `/memory/index` | Index files and add them to memory.yaml |
| `/memory/search` | Search for relevant memory entries by keyword |
| `/memory/diff` | Detect and list missing memory entries |
| `/memory/validate-files` | Ensure listed files actually exist in memory + Git |
| `/audit/validate_changelog` | Backfill any missing changelog entries based on outputs |
| `/git/rollback_commit` | Roll back one or more files from a previous commit |
| `/getFile` and `/batch-files` | Retrieve file content from GitHub (single or multiple) |
| `/actions/list` | Get all available tools grouped by category with descriptions |

Each tool maps to a route in the OpenAPI schema

---

## 📊 Logs & Reports

| File | What It Tracks |
|------|----------------|
| `changelog.yaml` | Every committed file |
| `reasoning_trace.yaml` | Thoughts, scores, and AI decision data |
| `metrics_report.yaml` | Project-level performance |
| `reverted_commits.yaml` | Undo history with reason |
| `handoff_notes.yaml` | Pod-to-pod task transitions |
| `chain_of_thought.yaml` | Inline reasoning log for each task |

---

## 🧭 Getting Started

Welcome! This AI assistant helps you run structured delivery tasks using GPT pods and tools.

### 🗣 Example Prompts to Try:
- “Start a new task”
- “What’s next in my delivery project?”
- “List all tools I can use”
- “Show me the current task queue”
- “What’s the summary for task 2.1?”

### 💡 You Can Ask GPT for Help Anytime:
- “What tools do I have?”
- “Remind me how to complete a task”
- “Where does chain_of_thought go?”

### 🧰 Developer Quick Actions

| **Prompt**            | **Description**                                      |
|------------------------|------------------------------------------------------|
| Call `/actions/list`   | Lists all tools available                            |
| Fetch `task.yaml`      | View all defined tasks                               |
| Start task 1.2         | Kicks off a task with prompt tracking                |
| Log an issue           | Append to `chain_of_thought` with issues and lessons |


---

## ✅ You’re Ready

You're now equipped to lead a structured, AI-native delivery flow. Guide the pods, review logs, and evolve your process over time.

Let the system handle the structure — and let your team do the thinking.
