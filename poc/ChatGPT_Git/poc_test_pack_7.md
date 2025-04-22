# 🧪 PoC Test Pack – Iterative Tasks 2.4 to 2.7

This test pack supports proof-of-concept runs for Tasks 2.4a, 2.4b, 2.5, 2.6, and 2.7 using the Memory Pod GPT + GitHub Tool integration.

---

## ✅ Objectives by Task

### 🧾 Task 2.4a – Fix Bugs from QA
**Goal:** Apply fixes for failed test cases, confirm with local test runs, update the spec, and generate a patch.

**Files:**
- `test/feature_<feature_id>/qa_test_results.md`
- `docs/specs/spec_<feature_id>.md`
- `src/feature_<feature_id>/`
- `tests/feature_<feature_id>/`
- `.patches/patch_<timestamp>.diff`

**Prompt:** Use `prompts/dev/2.4a_fix_bugs_from_qa.txt`

**Expected Outputs:**
- Updated source and test code
- Updated spec with implementation notes and test coverage
- Patch file saved to `.patches/`

---

### 🧾 Task 2.4b – Retest After Fixes
**Goal:** QA Pod verifies that all previously failed or blocked test cases now pass and updates acceptance status.

**Files:**
- `test/feature_<feature_id>/qa_test_results.md`
- `docs/qa/acceptance_matrix.md`
- `src/feature_<feature_id>/`
- `tests/feature_<feature_id>/`

**Prompt:** Use `prompts/qa/2.4b_retest_after_fixes.txt`

**Expected Outputs:**
- Updated `qa_test_results.md` with final test results
- Acceptance matrix marked as validated

---

### 🧾 Task 2.5 – Research Support
**Goal:** Investigate unresolved questions and technical gaps and document the findings as a research spike.

**Files:**
- `.logs/feedback/2.x_*.md`
- `docs/specs/spec_<feature_id>.md`
- `docs/qa/acceptance_matrix.md`
- `docs/research/spikes/<topic>.md`

**Prompt:** Use `prompts/research/2.5_research_assist.txt`

**Expected Outputs:**
- Well-documented research spike summarizing the question, findings, and proposed actions
- Cross-referenced spec and feedback log entries

---

### 🧾 Task 2.6 – Run Agile Rituals & Capture Metrics
**Goal:** Facilitate retro, update velocity and burndown charts, and summarize process insights.

**Files:**
- `.logs/feedback/2.*.md`
- `metrics/metrics.yaml`
- `docs/rituals/retrospective.md`
- `metrics/velocity.md`
- `metrics/burndown.md`

**Prompt:** Use `prompts/wow/2.6_agile_metrics.txt`

**Expected Outputs:**
- Retrospective markdown doc summarizing team learning
- Updated velocity and burndown metrics
- Feedback log entries capturing process gaps

---

### 🧾 Task 2.7 – Prepare Deployment Guide
**Goal:** Document full environment setup and steps to deploy feature(s), including validation checks.

**Files:**
- `docs/specs/spec_<feature_id>.md`
- `.patches/patch_<timestamp>.diff`
- `docs/deployment/deployment_guide.md`

**Prompt:** Use `prompts/dev/2.7_prepare_deployment_guide.txt`

**Expected Outputs:**
- Deployment guide with env setup, secrets, steps, and verification
- Final saved doc in `docs/deployment/`

---

## 🔁 Workflow
1. Run each task with DevPod, QAPod, ResearchPod, or WoWPod as appropriate
2. Use GitHub File Tool to fetch required inputs
3. Let GPT generate results and validate output
4. Save files and record feedback in `.logs/feedback/`

---

## 📁 Supporting File Checklist
Ensure the following are present or generated:
- `qa_test_results.md` (initial + updated)
- `acceptance_matrix.md`
- `spec_<feature_id>.md`
- `spikes/<topic>.md`
- `.patches/patch_<timestamp>.diff`
- `deployment_guide.md`
- `retrospective.md`, `velocity.md`, `burndown.md`

---

Let me know if you want to auto-generate test logs or add a `test_runner.py` script!