# 🛠️ SOP: Dev Pod

File: `/docs/wow/sop_dev_pod.md`

---

## 🎯 Pod Mission & Role
- Build the AI application components (code, logic, prompts, YAML specs, scripts)
- Translate features and specs into working functionality
- Collaborate closely with QA, Research, and Delivery pods
- Automate wherever possible

### 🔄 Lifecycle Role
- Kicks in after discovery to build the first working prototype
- Iterates each sprint based on backlog, changelog, and review feedback

---

## ✅ Default Tasks
- Implement new features from `feature_backlog.yaml`
- Create or update YAMLs (flows, prompts, metadata)
- Write reusable prompt functions or chains
- Maintain modular Python code in `/src`
- Document feature interfaces in markdown
- Generate structured test fixtures or data mocks for QA

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Backlog | `/docs/wow/feature_backlog.yaml` |
| Prompt Specs | `/data/prompts/*.yaml` |
| Architecture | `/docs/solution_architecture.md` |
| Code Base | `/src/`, `/scripts/`, `/data/` |
| Templates | `/docs/wow/templates/dev_feature.yaml`, `prompt_template.yaml` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Feature implementation | `.py`, `.yaml`, `.md` | `/src/`, `/data/`, `/docs/` | QA Pod, Delivery Pod |
| New prompt templates | `.yaml` | `/data/prompts/` | Research Pod, QA Pod |
| Structured feature interface doc | `.md` | `/docs/specs/` | All pods |
| Sprint changelog entry | `.md` | `/docs/changelog.md` | Human Lead, All pods |

---

## 🧪 Execution Standards
- Follows modular design (one feature = one file/folder)
- Uses type hints and docstrings
- Maintains clean file diffs for Git
- Avoids hardcoding — use config or structured YAML input
- Adds `# region` comments for ChatGPT-parsable chunks
- Prompt functions should separate template from logic

---

## 📁 Templates

### dev_feature.yaml
```yaml
feature_id: F4.3
name: Generate Return-to-Play Guidance
status: in_progress
owner: dev_pod
inputs:
  - assessment_data
  - protocol_yaml
outputs:
  - markdown_guidance
  - trace_log
related_files:
  - src/models/guidance_generator.py
  - data/protocols/return_to_play.yaml
notes: "LLM-guided synthesis step. Uses OpenAI + embedding search."
```

### prompt_template.yaml
```yaml
template_name: guidance_prompt
role: system
prompt:
  - "You are a medical assistant helping translate concussion protocols into user-friendly guidance."
  - "Input: {symptom_summary}"
  - "Task: Generate stage-appropriate return-to-play advice."
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Propose new YAML structures where needed
- Flag ambiguous requirements to Delivery Pod
- Version everything via Git-style folder structure

### ❌ Don’t:
- Write tests without input from QA Pod
- Invent new flows without checking end_to_end_flow.md
- Commit directly to `main` — use branches

---

Ready for execution 🚀

