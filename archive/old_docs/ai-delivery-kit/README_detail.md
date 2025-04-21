# 🧠 AI-Native Delivery System – Starter Repo

Welcome to the AI-native delivery system for building, shipping, and evolving intelligent applications with human + AI collaboration.

This repo serves as a modular foundation for delivering LLM-powered products using ChatGPT pods and structured knowledge artifacts.

---

## 🚀 Purpose
- Enable fast, traceable AI app delivery
- Empower solo builders and teams with AI-native workflows
- Replace traditional software silos with pod-based reasoning and shared memory

---

## 📁 Folder Structure
```
.
├── src/                     # Application source code
├── data/                    # YAML configs, prompt templates
├── docs/
│   ├── wow/                 # Playbooks, SOPs, templates
│   ├── research/            # Logs, briefs
│   ├── specs/               # Structured markdown specs
│   ├── status/              # Sprint and progress reports
├── outputs/                 # Generated reports
├── logs/                    # Trace logs, LLM diagnostics
├── notebooks/               # Optional scratchpads
├── scripts/                 # Shell helpers (e.g., deploy.sh, test.sh)
```

---

## ⚙️ How It Works
- You (the human) act as the project lead
- Each ChatGPT conversation represents a pod (Dev, QA, etc.)
- Pods follow [SOPs in `/docs/wow/`](./docs/wow/) and generate artifacts (YAMLs, code, markdown)
- All work is versioned in Git with traceability across pods, files, and sprints

---

## 📚 Key Files
- `docs/wow/playbook.md` – Main operating model
- `docs/wow/sop_<pod>.md` – SOPs for each pod
- `docs/wow/templates/` – Reusable templates (backlog, prompts, tests)
- `docs/status/changelog.md` – Sprint-by-sprint log

---

## ✅ Quickstart

### 1. 🧭 Run Discovery Phase
```bash
./scripts/run_discovery.sh
```
Creates:
- `feature_backlog.yaml`
- `solution_architecture.md`
- `research_log.md`

### 2. 🚀 Start Sprint
```bash
./scripts/start_sprint.sh
```
Sets up:
- `sprint_plan.yaml`
- `handoff_log.yaml`
- `status/weekly_report.md`

### 3. 🔁 Pod Handoffs
Each pod logs:
- Inputs used
- Files updated
- Outputs delivered

Updates `handoff_log.yaml` for tracking.

### 4. ✅ QA + Review
```bash
./scripts/run_tests.sh
```
Validates:
- Flow behavior
- Prompt correctness
- Output reasoning

---

## 🧠 Supported Pod Types
- `dev_pod`: Build features, code, YAMLs
- `qa_pod`: Write and run tests
- `research_pod`: Extract and structure knowledge
- `delivery_pod`: Plan sprints, maintain backlog
- `wow_pod`: Maintain SOPs, logs, rituals

---

## 🧰 Tools Used
- Git + GitHub
- OpenAI + embeddings
- YAML + Markdown
- Optional: Streamlit, FastAPI, Docker, LangChain

---

## 💡 Philosophy
- Every pod is traceable
- Every thought has a file
- Every decision is written down

Let’s ship smart, fast, and together 🚢🤖

