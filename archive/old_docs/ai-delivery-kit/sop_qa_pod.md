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

