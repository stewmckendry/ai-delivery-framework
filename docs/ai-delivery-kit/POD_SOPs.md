# 🧠 POD SOPs – How Pods Operate


## Sop Delivery Pod

# 🚚 SOP: Delivery Lead Pod

File: `/docs/wow/sop_delivery_pod.md`

---

## 🎯 Pod Mission & Role
Owns the overall plan and delivery rhythm. Turns discovery and sprint activities into forward momentum and structured outputs.

### 🔄 Lifecycle Role
- Leads planning during Discovery and each Sprint 0
- Owns the feature backlog, roadmap, and coordination
- Works closely with Human Lead and WoW Pod to steer delivery cadence

---

## ✅ Default Tasks
- Maintain and groom `feature_backlog.yaml`
- Run or document sprint planning in `sprint_plan.yaml`
- Align pod responsibilities per feature
- Draft changelog entries and ensure handoffs are logged
- Track completion, gaps, and carry-forward items

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Backlog | `/docs/wow/feature_backlog.yaml` |
| Sprint Plan | `/docs/wow/sprint_plan.yaml` |
| Changelog | `/docs/changelog.md` |
| Pod SOPs | `/docs/wow/sop_*.md` |
| QA Feedback | `/docs/qa/results/`, `defect_log.yaml` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Updated backlog | `.yaml` | `/docs/wow/` | All pods |
| Sprint plan | `.yaml` | `/docs/wow/` | Dev, QA Pods |
| Changelog | `.md` | `/docs/` | Human Lead |
| Delivery summary | `.md` | `/docs/status/weekly_report.md` | All pods, Human Lead |

---

## 🧪 Execution Standards
- Each feature must have a status and pod owner
- All file changes should have a changelog entry
- Delivery decisions should be documented in markdown
- Sprint YAMLs must be self-contained and editable

---

## 📁 Templates

### sprint_plan.yaml
```yaml
sprint_id: S2
start_date: 2025-04-22
end_date: 2025-04-29
goals:
  - Complete QA on RTP guidance
  - Begin UI sketching for new intake form
features:
  - id: F3.2
    pod_owner: qa_pod
  - id: F1.1
    pod_owner: dev_pod
milestones:
  - name: Feature test complete
    due: 2025-04-25
    related_to: F3.2
```

### changelog.md
```md
## Sprint 2 - April 22–29

### ✨ Added
- `guidance_generator.py` to `src/models`
- New YAML template for RTP stages

### 🐛 Fixed
- LLM fallback logic for empty symptom list

### 🔄 Changed
- Updated `return_to_play.yaml` to include progression criteria
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Track pod capacity and progress per sprint
- Propose pruning or grouping of features
- Maintain handoff traceability across pods

### ❌ Don’t:
- Write production code
- Rewrite research or prompts without collaboration
- Skip changelog updates or documentation

---

Delivery is not just a deadline — it's a design 🗺️



## Sop Dev Pod

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



## Sop Discovery Phase

# 🔍 SOP: Discovery Phase

File: `/docs/wow/sop_discovery_phase.md`

---

## 🎯 Purpose & Goals
The Discovery Phase exists to:
- Frame the user problem and intended outcomes
- Understand constraints (tech, data, timeline)
- Validate feasibility with lightweight research
- Define an initial solution architecture
- Produce sprint-ready artifacts

---

## 🚀 Outputs
| Artifact | Format | Path |
|----------|--------|------|
| Discovery Report | `.md` | `/docs/discovery/discovery_report.md` |
| Research Log | `.md` | `/docs/research/research_log.md` |
| Feature Backlog | `.yaml` | `/docs/wow/feature_backlog.yaml` |
| Solution Architecture | `.md` | `/docs/solution_architecture.md` |
| End-to-End Flow | `.md` | `/docs/end_to_end_flow.md` |
| Data Model | `.yaml` | `/data/model/data_model.yaml` |
| Risk Log | `.md` | `/docs/discovery/risk_log.md` |
| Sprint Plan | `.yaml` | `/docs/wow/sprint_plan.yaml` |

---

## 👥 Active Pods
| Pod | Responsibility |
|-----|----------------|
| Research Pod | Evidence gathering, benchmark scans |
| Delivery Pod | Backlog creation, architecture definition |
| WoW Pod | Templates, structure, logging setup |

---

## 🪜 Transition to Sprint
1. Review discovery artifacts with Human Lead
2. Refine backlog items and assign initial pod owners
3. Create first `sprint_plan.yaml`
4. Update `changelog.md` to note discovery completion
5. Kick off Sprint 0

---

## 📑 Example Template: feature_backlog.yaml
```yaml
features:
  - id: F1.1
    name: Concussion Intake Form
    pod_owner: dev_pod
    status: not_started
    priority: high
    dependencies: []
    description: "Form for capturing user input on possible concussion events."
    discovery_notes: "SCAT6 protocol reference, YAML-driven layout"
```

---

Discovery is your north star 🌟 — don’t skip it.



## Sop Qa Pod

# ✅ SOP: QA Pod

File: `/docs/wow/sop_qa_pod.md`

---

## 🎯 Pod Mission & Role
Ensure that every AI feature or component functions as expected, handles edge cases, and produces trustworthy, traceable results.

### 🔄 Lifecycle Role
- Enters after Dev Pod submits a new feature or change
- Operates during each sprint to validate feature functionality
- Conducts regression testing before releases

---

## ✅ Default Tasks
- Define test cases per feature in `test_cases.md`
- Run manual or scripted tests for YAML flows, reasoning paths
- Validate prompt output correctness and stability
- Review logs, thought traces, and intermediate steps
- Flag issues to Dev and Delivery Pods

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Features | `/docs/wow/feature_backlog.yaml` |
| Test Cases | `/docs/qa/test_cases.md` |
| Output Files | `/outputs/*`, `/logs/*` |
| Prompt Specs | `/data/prompts/*.yaml` |
| Dev Outputs | `/src/**/*.py`, `/data/**/*.yaml` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| QA Results | `.md` | `/docs/qa/results/feature_<id>.md` | Dev, Delivery Pods |
| Regression Report | `.md` | `/docs/qa/reports/` | Delivery Pod |
| Defect Log | `.yaml` | `/docs/qa/defect_log.yaml` | Dev Pod |
| Feedback Comments | Inline in test files or via changelog | Dev, Delivery |

---

## 🧪 Execution Standards
- Follow Given/When/Then format for test cases
- Use “confidence”, “expected vs. actual” metrics for LLM validations
- Report at least one log or output trace per feature tested
- Version test cases alongside feature versions

---

## 📁 Templates

### test_cases.md
```md
## F3.2 - Generate Return-to-Play Guidance

### Test 1: Base Case
- Input: symptoms = [headache, light sensitivity], day_post_injury = 5
- Expected Output: summary includes "Stage 2", guidance is readable
- Result: ✅ Passed

### Test 2: Edge Case - Missing data
- Input: symptoms = [], day_post_injury = null
- Expected Output: summary requests clarification or gives minimal advice
- Result: ❌ Failed - GPT defaulted to generic answer
- Notes: needs fallback handler in guidance_generator.py
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Log QA rationale for LLM judgments
- Use markdown tables for structured results
- Confirm that all reasoning steps are visible

### ❌ Don’t:
- Assume correctness from Dev — re-test every time
- Skip YAML field validation (structure, type, required)
- Modify source code directly

---

QA is the conscience of the code 🧪



## Sop Research Pod

# 🔬 SOP: Research Pod

File: `/docs/wow/sop_research_pod.md`

---

## 🎯 Pod Mission & Role
Collect, synthesize, and structure knowledge relevant to user needs, problem context, AI techniques, and best practices.

### 🔄 Lifecycle Role
- Active in Discovery Phase
- Supports all pods during sprints with focused investigations or source reviews
- Maintains structured knowledge base for reuse

---

## ✅ Default Tasks
- Write research briefs on AI methods, tools, UX/clinical best practices
- Extract structured data from protocols, standards, or references
- Evaluate LLM performance across known benchmarks or heuristics
- Support prompt refinement, scoring frameworks, evaluation metrics

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Research prompts | `/data/prompts/research_queries.yaml` |
| Source docs | `/docs/research_sources/`, `.pdf` uploads |
| Knowledge logs | `/docs/research/research_log.md` |
| Evaluations | `/outputs/eval/`, `/logs/llm_eval/*.md` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Research log | `.md` | `/docs/research/research_log.md` | WoW, Delivery Pods |
| Structured YAML data | `.yaml` | `/data/reference/` | Dev Pod, QA Pod |
| Research briefs | `.md` | `/docs/research/briefs/` | All pods |
| Prompt references | `.yaml` | `/data/prompts/` | Dev Pod, QA Pod |

---

## 🧪 Execution Standards
- Use citation format: `Author (Year) - Title`
- Highlight risks, trade-offs, bias, or quality caveats
- Link research logs to feature backlog entries where relevant
- Maintain prompt hygiene (clarity, roles, token-efficient)

---

## 📁 Templates

### research_log.md
```md
## Entry: Return-to-Play Guidelines (F4.1)
- Goal: Extract stages from Canadian RTP PDF
- Sources: Parachute (2019), CDC HEADS UP
- Summary: 6-stage progression with activity descriptions and criteria
- Output file: `/data/protocols/return_to_play.yaml`
- Linked to: `feature_backlog.yaml > F4.1`
```

### research_data.yaml
```yaml
reference: return_to_play
source: parachute_canada
stages:
  - id: stage_1
    name: Symptom-limited activity
    description: "Daily activities that do not provoke symptoms"
    allowed_activities:
      - "Short walks"
      - "Reading"
    progression_criteria:
      - "Symptoms are improving"
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Link every research finding to a feature or decision
- Structure findings in YAML when possible
- Flag when evidence is weak or speculative

### ❌ Don’t:
- Generate prompts without Dev Pod input
- Make final architectural or coding decisions
- Use GPT results without tracing sources

---

Knowledge fuels capability 🔎



# ⚙️ SOP: WoW (Ways of Working) Pod

File: `/docs/wow/sop_wow_pod.md`

---

## 🎯 Pod Mission & Role
Design and maintain the AI-native operating system used by all pods and the human. Owns playbooks, SOPs, workflows, and pod health.

### 🔄 Lifecycle Role
- Active in Discovery to frame structure and standards
- Operates continuously to evolve best practices
- Serves as system architect for ways-of-working, handoffs, memory, and traceability

---

## ✅ Default Tasks
- Maintain the `playbook.md` and all `sop_*.md` files
- Define templates and folder structure conventions
- Propose pod prompts, rituals, and handoff formats
- Track pod-to-pod and human-AI collaboration quality
- Coordinate research into tooling and automation improvements

---

## 🧰 Tools & Inputs
| Source | Example |
|--------|---------|
| Existing SOPs | `/docs/wow/sop_*.md` |
| Playbook | `/docs/wow/playbook.md` |
| Logs | `/logs/**/*.md`, `handoff_log.yaml` |
| Delivery Outputs | `/docs/status/`, `changelog.md` |

---

## 📤 Outputs
| Output | Format | Destination | Recipient |
|--------|--------|-------------|-----------|
| Updated playbook | `.md` | `/docs/wow/` | All pods |
| New/Updated SOPs | `.md` | `/docs/wow/sop_*.md` | All pods |
| Templates | `.md`, `.yaml` | `/docs/wow/templates/` | Dev, QA, Delivery Pods |
| Ways of Working Report | `.md` | `/docs/status/wow_report.md` | Human Lead |

---

## 🧪 Execution Standards
- Keep all process documentation human-readable AND ChatGPT-friendly
- Use markdown structure with YAML examples for clarity
- Document all pod rituals, formats, and expectations
- Maintain shared vocabulary across prompts, logs, flows

---

## 📁 Templates

### wow_report.md
```md
## WoW Report – Sprint 2

### 🚧 Pain Points
- QA pod unclear on how to validate prompt correctness

### ✅ Improvements
- Added "confidence field" convention to all thought outputs
- QA test case template expanded with Given/When/Then format

### 📌 Next Iterations
- Create guidance for multi-agent reasoning memory traces
```

### handoff_log.yaml
```yaml
handoffs:
  - from: dev_pod
    to: qa_pod
    date: 2025-04-20
    files:
      - src/models/guidance_generator.py
      - data/prompts/guidance_prompt.yaml
    notes: "Needs QA review of symptom fallback"
```

---

## 🙅 Do/Don’t

### ✅ Do:
- Proactively propose workflow changes
- Codify what worked and why
- Use sprint logs and changelogs to guide improvement

### ❌ Don’t:
- Override pod responsibilities without review
- Assume process fit without real usage feedback
- Drift away from what’s executable

---

Ways of Working is the source code of collaboration ⚙️




# 🧠 POD SOPs – How Pods Operate

This guide defines the role, inputs, outputs, and standard rituals for each pod using the AI Delivery Kit. Every pod knows exactly:
- What to do
- What files to expect and produce
- Where to find and place them in Git
- What templates to follow
- How to escalate if context is missing

---

## 🔁 How It Works
Each pod:
1. Pulls latest files from `main` before work
2. Loads required **inputs** from Git
3. Escalates to the Delivery Lead if required inputs are missing or unclear
4. Generates required **outputs** to Git using defined formats
5. Submits a patch using `generate_patch.py` with:
   - `logs/changelog.yaml` update
   - `logs/thought_trace.yaml` entry
   - `logs/handoff_log.yaml` if assigning work to another pod

---

## 🧪 Pod: DEV
### 🎯 Job: Build Features

**Inputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Feature Spec | `.md` | `feature_spec_*.md` | `docs/specs/` | `feature_spec_template.md` |
| Prompt Spec | `.yaml` | `*.yaml` | `data/prompts/` | `prompt_template.yaml` |
| Backlog | `.yaml` | `feature_backlog.yaml` | `docs/wow/` | `backlog_template.yaml` |

**Outputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Source Code | `.py` | `*.py` | `src/` | `dev_feature_template.py` |
| Prompt YAML | `.yaml` | `*.yaml` | `data/prompts/` | `prompt_template.yaml` |
| Feature Spec (Updated) | `.md` | `feature_spec_*.md` | `docs/specs/` | appended tech notes |
| Thought Trace | `.yaml` | `thought_trace.yaml` | `logs/` | auto-generated |

---

## 🧪 Pod: QA
### 🎯 Job: Design and Execute Tests

**Inputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Feature Code | `.py` | `*.py` | `src/` | Dev output |
| Prompt YAML | `.yaml` | `*.yaml` | `data/prompts/` | Prompt spec |

**Outputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Test Plan | `.md` | `test_cases.md` | `docs/qa/` | `test_plan_template.md` |
| QA Results | `.md` | `feature_*.md` | `docs/qa/results/` | `qa_results_template.md` |
| Defect Log | `.yaml` | `defect_log.yaml` | `docs/qa/` | YAML format |
| Thought Trace | `.yaml` | `thought_trace.yaml` | `logs/` | auto-generated |

---

## 🔬 Pod: RESEARCH
### 🎯 Job: Extract and Structure Useful Knowledge

**Inputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Source Material | `.pdf`, `.md` | `*.pdf`, `*.md` | `docs/research_sources/` | none |
| Prompt Template | `.yaml` | `*.yaml` | `data/prompts/` | `prompt_template.yaml` |

**Outputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Research Brief | `.md` | `brief_*.md` | `docs/research/briefs/` | `brief_template.md` |
| Structured Data | `.yaml` | `*.yaml` | `data/reference/` | `research_data.yaml` |
| Thought Trace | `.yaml` | `thought_trace.yaml` | `logs/` | auto-generated |

---

## 🪩 Pod: WOW
### 🎯 Job: Improve the System, Rituals, and Velocity

**Inputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Feedback | `.md` | `PATCH: WOW_FEEDBACK.md` | `.patches/` | freeform |
| Logs | `.yaml` | `*.yaml` | `logs/`, `.metrics/` | system-generated |

**Outputs**
| Name | File Type | File Pattern | Location | Template Ref |
|------|-----------|---------------|----------|----------------|
| Updated SOPs | `.md` | `POD_SOPs.md` | `docs/` | n/a |
| Scripts | `.py`, `.sh` | `*.py`, `*.sh` | `scripts/` | system tools |
| Init Patch | `.diff` | `*.diff` | `.patches/` | `generate_patch.py` |
| Thought Trace | `.yaml` | `thought_trace.yaml` | `logs/` | auto-generated |

---

## 📚 Reference: How Pods Get Files from Git

See: [`docs/Pods_GET_Guide.md`](Pods_GET_Guide.md)

- Pods must sync before work: `git checkout main && git pull`
- All expected inputs should be present
- If missing or unclear, escalate to Delivery Lead

> Use `scripts/load_context.py` to standardize loading inputs.

---

