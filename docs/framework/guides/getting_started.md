# 🚀 Getting Started with AI-Native Delivery

Welcome to the future of AI-powered teamwork!  
This guide helps new **Pods**, **Human Leads**, and **Project Teams** start using the AI-Native Delivery Framework.

---

## 1. User View: Who You Are

| Role | What You Do First |
|:---|:---|
| GPT Pod | Connect to FastAPI, activate your first task |
| Human Lead | Review backlog, activate tasks, supervise reasoning traces |
| Project Team | Understand the flow: tasks ➔ outputs ➔ patches ➔ retrospectives |

---

## 2. Process View: How to Begin

1. Clone the project repository.
2. Review available tasks using `/tasks/list`.
3. Activate your first task via `/tasks/activate`.
4. Review prior memory using `/memory/search` or manual browsing.
5. Generate outputs + reasoning.
6. Promote outputs via `/patches/promote`.

---

## 3. Data & AI View: What's Happening Behind the Scenes

- Tasks are structured in `task.yaml`.
- Memory items are indexed in `memory.yaml`.
- Reasoning traces captured in `.logs/reasoning/`.
- Metrics begin accumulating as you work.

---

## 4. Technology Stack View: What Powers This

| Layer | Tech |
|:---|:---|
| API Access | FastAPI server (e.g., Railway) |
| Repo Management | GitHub for tasks, outputs, memory |
| Patch Promotion | PyGitHub + FastAPI `/patches/promote` |
| Prompt Management | GitHub file retrieval via FastAPI |

---

## 5. Example: Pod First Activation

1. DeliveryPod runs `/tasks/activate` for `2.1_capture_project_goals`.
2. Fetches related memory entries on project vision.
3. Produces an updated goals document + reasoning trace.
4. Calls `/patches/promote` to submit the patch.
5. Human Lead reviews patch and merges.

---

# 🏁 You're now part of an AI-native team.
