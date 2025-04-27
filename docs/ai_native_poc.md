# 🎯 PoD Mission: PoC Field Test — Build a Complete AI Micro-App (Inspired by Coaching the Machine + NHL Playoffs)

You are tasked with delivering a complete, working AI-powered micro-application using our AI-Native Delivery System.

The goal: **showcase the power of modular AI-native delivery** — fast, traceable, playful, and real.

---

## 🧾 Field-Test Workflow

### 1. Understand the Field-Test Goals
- Build something simple, real, and demonstrable.
- Move fast: prioritize modular work and traceability over polish.
- Capture learnings: identify bottlenecks, friction points, improvement ideas.
- Prove how AI-native delivery accelerates real-world app building.

### 2. Select an Initial App Idea — Coaching the Machine meets NHL Playoffs!
- Align with the Coaching the Machine philosophy: teaching, guiding, assisting through lightweight, intelligent tools.
- Stay playful and current: theme around the NHL Playoffs!

**Suggested App Ideas:**
- 🏒 **Playoff Predictor:** Enter game results and predict playoff bracket scenarios.
- 🏒 **Hockey Game Summary Bot:** Input game recaps; generate summaries in fan, coach, or analyst tone.
- 🏒 **Coach’s Quick Scout:** Upload simple stats or notes; generate scouting reports or pre-game plans.
- 🏒 **Fan Assistant:** Get upcoming schedules, key players, series breakdowns — in a fun or serious tone.

✅ **If unsure:** Propose 2–3 options to the Human Lead for quick selection.

### 3. Spin Up the Project Repository Structure
- Separate framework code from project-specific files.

**Example Structure:**
/framework/         (AI delivery system — DO NOT EDIT)
/project1_nhl_poc/
    ├── src/
    ├── data/
    ├── outputs/
    ├── prompts/
    ├── task.yaml
    ├── memory.yaml
    ├── notebooks/
    ├── .logs/
    └── README.md


### 4. Initiate Work Using the Delivery Framework
- Create and activate tasks via `task.yaml`.
- Validate inputs (`memory.yaml`, GitHub file fetch).
- Work modularly: small patches, frequent promotions.
- Use `promote_patch` tool after completing each modular deliverable.
- Generate reasoning traces and handoff notes for each patch.

### 5. Use Custom GPT Pods Where Applicable
- Activate ProductPod, ResearchPod, QAPod, DeliveryPod, WriterPod as needed.
- Use standard system prompts and custom actions.

### 6. Track Field Observations
- Create a `field_test_observations.md` file tracking:
  - What worked well
  - Where friction occurred
  - Opportunities to improve the framework, pods, memory, handoffs

### 7. Prepare a Showcase Summary
**Final Outputs:**
- ✅ Working micro-app
- ✅ Full patch + reasoning trace trail
- ✅ Metrics collected (velocity, quality, thoughtfulness)
- ✅ Field test observations and retrospective

---

## 📎 Special Instructions

- Move fast but stay modular (small promotable patches).
- Embed coaching-style thinking: "guide, don't dictate."
- Highlight AI-native benefits — and note any weaknesses.
- Capture the spirit of playfulness, learning, and teamwork — like a great playoff run!

> 🏒🚀 **You’re not just building a tool — you’re field-testing the future of delivery.**

---

# 📦 Briefing Package for the PoC Field Test

| **Section**          | **Contents**                                                                 |
|-----------------------|------------------------------------------------------------------------------|
| **Goal**              | Build and deliver a working AI micro-app using the full AI-native framework  |
| **Output Artifacts**  | `src/`, `data/`, `outputs/`, `prompts/`, `task.yaml`, `memory.yaml`, `.logs/`, `README.md`, final app |
| **Supporting Pods**   | ProductPod, ResearchPod, QAPod, DeliveryPod, WriterPod                      |
| **Metrics**           | Use MVP metrics framework to capture velocity, cycle time, reasoning quality |
| **Deliverables**      | App code + system artifacts + `field_test_observations.md` + PR trail         |
| **Success Criteria**  | App delivered; framework proven; learnings captured                         |
| **Constraints**       | Lightweight, modular, frictionless                                           |

