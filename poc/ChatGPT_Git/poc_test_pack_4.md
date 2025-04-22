# 🧪 PoC Test Pack – Discovery Tasks 1.2 to 1.4

This test pack supports proof-of-concept runs for Tasks 1.2, 1.3, and 1.4 using the Memory Pod GPT + GitHub Tool integration.

---

## ✅ Objectives by Task

### 🧾 Task 1.2 – Define User & Delivery Flows
**Goal:** Populate `user_roles.md`, `app_walkthrough.md`, and `delivery_flow.md` with complete metadata for user personas, journeys, and SDLC pods.

**Files:**
- `docs/personas/user_roles.md`
- `docs/journeys/app_walkthrough.md`
- `docs/workflows/delivery_flow.md`

**Prompt:** Use the full template from `prompts/dev/define_user_and_delivery_flows.txt`

**Expected Outputs:**
- Completed markdown files for user roles, app journeys, and delivery flow
- GPT-generated summaries and clarifications for discussion

---

### 🧾 Task 1.3 – Break Into Features
**Goal:** Propose 3–7 features based on goals, personas, and journey data, each with structured metadata.

**Files:**
- `docs/project_goals.md`
- `docs/personas/user_roles.md`
- `docs/journeys/app_walkthrough.md`

**Prompt:** Use the full template from `prompts/dev/break_into_features.txt`

**Expected Outputs:**
- One or more `docs/features/feature_*.md` files
- Feature metadata including ID, user story, ACs, personas, journey stage, etc.

---

### 🧾 Task 1.4 – Write Acceptance Criteria
**Goal:** Extract or propose detailed, testable acceptance criteria for features, structured in markdown.

**Files:**
- `docs/features/feature_*.md`
- `docs/qa/acceptance_matrix.md`

**Prompt:** Use the full template from `prompts/qa/write_acceptance_criteria.txt`

**Expected Outputs:**
- Updated `acceptance_matrix.md`
- Structured ACs using `given/when/then`, metadata (e.g., status, priority, testable)

---

## 🔁 Workflow
1. Run each prompt via DevPod or QAPod
2. Allow GPT to retrieve inputs using the GitHub tool
3. Review generated outputs
4. Save outputs to the repo (manual or patch tool)
5. Log feedback to `.logs/feedback/task_id.md`

---

## 📁 Supporting File Checklist (Ensure These Are Committed)
- `docs/project_goals.md`
- `docs/personas/user_roles.md`
- `docs/journeys/app_walkthrough.md`
- `docs/workflows/delivery_flow.md`
- `docs/features/feature_*.md` (after Task 1.3)
- `docs/qa/acceptance_matrix.md`

---

Let me know if you’d like a feedback capture template, patch helper, or test log summary script!


# 📁 Data Stubs – Supporting Files for Tasks 1.2 to 1.4 PoC

These markdown files act as lightweight stubs to enable PoC testing for Tasks 1.2–1.4.

---

## 📄 docs/project_goals.md
```markdown
# Project Goals

This project aims to streamline how AI agents assist with collaborative software delivery. Key goals include:
- Reduce manual overhead in SDLC rituals
- Empower GPT-based Pods to execute and document work
- Use Git + Memory as a shared source of truth
- Provide traceability across tasks, thoughts, and decisions
```

---

## 📄 docs/personas/user_roles.md
```markdown
# User Roles

## Coach
- Helps athletes log symptoms and manage recovery

## Athlete
- Completes assessments and tracks recovery

## Clinician
- Reviews reports and signs off return-to-play
```

---

## 📄 docs/journeys/app_walkthrough.md
```markdown
# Application Walkthrough

## Onboarding Journey (Athlete)
- Starts with symptom entry
- Completes baseline checks
- Receives next-step guidance

## Report Review (Clinician)
- Enters via alert or dashboard
- Views submitted reports
- Signs off or sends follow-up
```

---

## 📄 docs/workflows/delivery_flow.md
```markdown
# Delivery Flow – AI-Native Operating System

1. Discovery (define goals, flows, features)
2. Iterative Development (DevPod, QAPod, ResearchPod)
3. Testing & Review
4. Git-based Patch Promotion
5. Feedback, Metrics, and Delivery Log
```

---

## 📄 docs/features/feature_sample.md
```markdown
# Feature: Guided Symptom Entry

- Feature ID: FTR-001
- Description: Athlete is guided through symptom questions
- User Story: As an athlete, I want a structured way to log how I feel
- Journey Stage: Onboarding
- Personas: Athlete
```

---

## 📄 docs/qa/acceptance_matrix.md
```markdown
# QA Acceptance Matrix

| Feature ID | Criteria ID | Description | Status |
|------------|-------------|-------------|--------|
| FTR-001    | AC-001      | Athlete sees list of symptoms | Pending |
```

Let me know if you want these saved to files, converted to patches, or tested with DevPod/QAPod!
