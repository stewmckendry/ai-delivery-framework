# 🧠 AI-Native Delivery System – Mission, Plan & Status Tracker

## 🎯 Mission
To build a fully modular, memory-driven, and patch-based AI-native delivery system where:
- Each **Pod** (DevPod, QAPod, ResearchPod, etc.) is a role-specific Custom GPT
- Work is defined via structured `task.yaml` and `memory.yaml`
- Inputs are retrieved via live GitHub memory (via tool)
- Pods reason and generate outputs automatically
- A human-in-the-loop iterates and approves changes
- All changes are committed via diff-based patching
- Logs, changelogs, and metrics are updated after each task

---

## 🛠️ Phases & Components

### 🧪 PoC Test Results
- ✅ Task 1.1: Capture Project Goals – Successful end-to-end run
  - GitHub file retrieved via tool
  - GPT generated clear summary + proposed rewrite
  - Conversational feedback loop enabled
  - Failure handling validated (404 error on missing file with clear recovery)


### ✅ Phase 0: Core Tooling Foundation *(Completed)*
- [x] GitHub File Proxy (FastAPI + Railway)
- [x] OpenAPI Schema + GPT Tool integration
- [x] `GET` and `POST /batch-files` endpoints

### 🔨 Phase 1: Standardized Task Framework
- [ ] Define SDLC task templates for each Pod
- [ ] Create `task_templates/` and `memory_templates/`
- [ ] Add quickstart docs per Pod

### 🔨 Phase 2: Prompt Generator
- [ ] Script to generate GPT prompt from `task.yaml` + `memory.yaml`
- [ ] Human-editable before sending to GPT
- [ ] Store in `prompts/` or generate inline

### 🔨 Phase 3: Patch Generation + Application
- [ ] `generate_patch.py` tool (already scoped)
- [ ] `apply_patch.py` to move .diff into repo + commit/PR
- [ ] Integrate with GitHub Actions or local scripts

### 🔨 Phase 4: Output Logging + Metrics
- [ ] Create structure for:
  - `changelog.md`
  - `trace_log.md`
  - `metrics.yaml`
- [ ] Add update scripts per Pod run

### 🔄 Phase 5: Human Feedback Loop
- [ ] Define review/approve cycle per Pod type
- [ ] Capture user feedback inline with GPT history
- [ ] Annotate output improvements and record decisions

### 🧪 Phase 6: End-to-End Demo Project
- [ ] Complete app delivery using AI-native system
- [ ] Show task → pod → patch → PR → merge → metrics

### Other Tasks Added During Build...
- [ ] Create centralized `prompts/` folder for live project use
- [ ] Move prompts/dev/capture_project_goals.txt from task template if ready for live run

---

## 📍 Current Status: **Batch File Retrieval Enabled**
- DevPod tested with `GET` and `POST` Git tool
- Prompt generator and patch writer are next
- Project tracking now formalized

---

## ✍️ Notes
- This file will be updated regularly with checkboxes
- Future improvements will include pod-specific tuning, patch review UX, and cross-pod coordination

Let’s build the future of delivery, one task at a time 🚀
