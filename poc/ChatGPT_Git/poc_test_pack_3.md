# 🧪 PoC Test Pack – Task 1.1: Capture Project Goals

This test validates the Memory Pod + Git Tool + Prompt execution for Discovery task 1.1.

---

## 🎯 Objective
Have **DevPod** retrieve the current `docs/project_goals.md` file and:
- Summarize the goals of the project
- Identify gaps or ambiguities
- Propose a revised version of the file

---

## 🧾 TASK YAML (input to DevPod)
```yaml
task_id: 1.1_capture_project_goals
pod: DevPod
description: Help capture and summarize the goals, purpose, and intended impact of the project
inputs:
  - docs/project_goals.md
```

---

## 📁 MEMORY YAML (used by file tool)
```yaml
- path: poc/test_data/docs/project_goals.md
  repo: stewmckendry/ai-concussion-agent
```

---

## 📡 TOOL USE
Use the **GET /repos/{owner}/{repo}/contents/{path}** endpoint via the GitHub File Tool to fetch:
- `docs/project_goals.md`

---

## 🧠 POD PROMPT (paste into DevPod)
*Note: This prompt is based on the prompt_template file at `task_templates/discovery/1.1_capture_project_goals/prompt_template.md`*

```markdown
🎯 POD MISSION: DevPod – Capture Project Goals

🧾 TASK YAML:
task_id: 1.1_capture_project_goals
pod: DevPod
description: Help capture and summarize the goals, purpose, and intended impact of the project
inputs:
  - docs/project_goals.md

📁 MEMORY:
- path: docs/project_goals.md
  repo: stewmckendry/ai-concussion-agent

📡 TOOL USE:
Use the GitHub File Tool’s GET /repos/.../contents/... endpoint to fetch the input file. Then:

1. Summarize the goals in 3–5 bullet points:
   - What is the project?
   - Who is it for?
   - Why does it matter?
   - What outcomes are we aiming for?
2. Identify any ambiguities or gaps to discuss with the human
3. Propose a refined version of `docs/project_goals.md` formatted in markdown
```

---

## ✅ Expected Outputs
- `project_goals_summary.md`: summary bullets
- `docs/project_goals.md`: rewritten file
- Optional: list of clarifying questions

---

## 📁 Supporting File (manually verify it's committed)
```markdown
📄 poc/test_data/docs/project_goals.md

# Project Goals (DRAFT)
This project aims to explore how we can use AI agents and memory-aware tools to build and ship software in a modular, automated way. Our goals include:
- Creating reusable tasks and memory templates
- Enabling dynamic GPT pods to reason from GitHub memory
- Generating useful outputs such as patches, tests, and feedback summaries
- Demonstrating how AI-native delivery can reduce time and cognitive load
```


Let’s run it and validate end-to-end reasoning flow from memory to patch! ✅
