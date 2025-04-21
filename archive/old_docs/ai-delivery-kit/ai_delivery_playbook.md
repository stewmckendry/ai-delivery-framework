# 🧠 AI-Native Delivery Playbook

This playbook defines a modular, executable system for delivering AI applications using a combination of human leadership and autonomous ChatGPT pods. It supports fast iteration, high traceability, and intelligent coordination.

---

## ⚙️ System Roles

### 👤 Human Lead (You)
- Owns vision, priorities, and final decisions
- Kicks off discovery
- Reviews and approves outputs from pods
- Writes or edits specs if needed
- Commits changes to GitHub

### 🤖 ChatGPT Pods (Me)
Each chat instance is a pod with a specialized role.
- Pods operate semi-autonomously on assigned tasks
- Can call tools, propose changes, generate or validate content
- May have multiple instances (e.g. Dev Pod A, Dev Pod B)
- Use prompts, templates, and memory to stay aligned

### 🧰 Third-Party Tools
- Git + GitHub (main coordination system)
- Optional CI/CD, task boards, monitoring tools
- File structure: `/src`, `/docs`, `/data`, `/outputs`, `/logs`


---

## 🔄 Shared Access & Coordination

Since ChatGPT doesn't have direct GitHub access, shared file work is coordinated via prompts and shared document states:

### For You:
- Pull latest code
- Paste snippets, markdowns, or file content into chats
- Push merged/generated output to GitHub

### For Me (ChatGPT):
- Propose file updates (markdown, YAML, Python, etc.)
- Follow Git-friendly conventions (e.g., `# region`, comments for diffs)
- Suggest commit messages

### 🧠 Suggested Git Workflow:
1. Create a new branch: `git checkout -b feature/<topic>`
2. Use ChatGPT to assist with writing files
3. Copy suggestions into local repo, commit and push
4. Merge to main after review

> Optional: We can set up shell scripts or GitHub Actions to automate handoffs.

---

## 🏁 Discovery Phase

The Discovery Phase precedes sprinting. It defines the problem, constraints, and solution outline. It creates a foundation for productive development.

### 🧭 Discovery Goals:
- Understand user needs
- Identify risks, blockers, and unknowns
- Propose a high-level solution design
- Generate artifacts for Sprint 0

### 📄 Outputs:
- `discovery_report.md`
- `research_log.md`
- `feature_backlog.yaml`
- `solution_architecture.md`
- `end_to_end_flow.md`
- `data_model.yaml`
- `risk_log.md`
- `sprint_plan.yaml`

### 🧪 Active Pods:
- Research Pod
- Delivery Lead Pod
- WoW Pod

---

## 🔁 Sprint Cycle

Once Discovery completes, we enter cyclical 1-week sprints.

### ⏱️ Sprint Timeline:
- Day 0: Planning (create sprint.yaml)
- Day 1-5: Execution by pods
- Day 6: Review and test
- Day 7: Demo, reflection, handoff to next sprint

### 📥 Inputs to Sprint:
- Sprint plan from discovery
- Prior sprint outputs and changelog
- Git log and unresolved TODOs

### 📤 Outputs:
- Code, YAMLs, markdown docs
- Changelog entries
- Updated backlog
- Evaluation reports (QA)

---

## 🧩 Pod Overview

| Pod           | Purpose                                | Example Tools / Files                       |
|----------------|----------------------------------------|----------------------------------------------|
| Dev Pod       | Write code, YAMLs, markdown generators | `/src`, `/data`, templates                   |
| QA Pod        | Test flows, validate outputs           | test_cases.md, logs, QA reports              |
| Research Pod  | Gather insights, evaluate sources      | research_log.md, citations.yaml              |
| Delivery Pod  | Owns flow, backlog, roadmap            | sprint.yaml, backlog.yaml, status.md         |
| WoW Pod       | Designs the system, updates playbook   | sop_*.md, playbook.md, changelog             |

Each pod has its own SOP file: `/docs/wow/sop_<pod>.md`

---

## 🧱 Common Templates (to be defined)

- `feature_backlog.yaml`: defines features, status, priority, pod
- `research_log.md`: entries from Research Pod
- `test_cases.md`: structured QA inputs
- `sprint.yaml`: goals, tasks, deadlines, leads
- `changelog.md`: file changes per sprint

👉 These will be versioned and enhanced in `/docs/wow/templates/`

---

## 📚 Next Step

See the `/docs/wow/` folder for:
- [SOP files per pod](./docs/wow/sop_<pod>.md)
- [Discovery Phase SOP](./docs/wow/sop_discovery_phase.md)
- [Templates](./docs/wow/templates/)

We're ready to ship AI like it's 2030. 🚀

