# 📚 Logs Overview – AI-Native Delivery System

This reference file explains the purpose, format, location, and usage process for each of the three main logs in the AI-native delivery system.

---

## 📒 Changelog

| Property | Details |
|----------|---------|
| **File** | `docs/changelog.md` |
| **Format** | Markdown (append-only) |
| **Purpose** | Track what changed, when, and why |
| **Updated By** | The pod proposing the change, or the human lead |
| **Used In** | Pull request summaries, retrospectives, audits |
| **Required in PRs** | ✅ Yes |

---

## 🧠 Thought Trace

| Property | Details |
|----------|---------|
| **File** | `logs/thought_trace.md` |
| **Format** | Markdown with optional YAML headers |
| **Purpose** | Capture reasoning behind changes and decisions |
| **Updated By** | Pod proposing change or human lead |
| **Used In** | PR body (via GitHub Action), documentation, learning loops |
| **Required in PRs** | ✅ Yes – at least one reasoning trace encouraged per patch |

---

## 🔁 Handoff Log

| Property | Details |
|----------|---------|
| **File** | `docs/wow/handoff_log.yaml` |
| **Format** | YAML list of handoffs |
| **Purpose** | Track file transitions between pods or human ↔ pod |
| **Updated By** | The pod initiating the handoff |
| **Used In** | GitHub PRs, pod metrics, delivery maps |
| **Required in PRs** | ✅ Yes – if patch is based on a handoff event |

---

## 🧭 Summary
All three logs are required parts of the AI-native workflow. They:
- Fuel GitHub automation and metrics
- Provide traceability
- Encourage thoughtfulness
- Help pods understand each other

Each pod SOP references which logs it contributes to.

> Logs are not documentation after-the-fact. They are the nervous system of the delivery engine.


## 🗂️ Question 1: Where Do the Logs Live?

✅ File + Folder Structure Recap
ai-native-delivery/
├── .patches/                         # Where GPT drops .diff patches
│   └── gpt_patch_f4.3.diff           # ← PATCH GOES HERE
│
├── docs/
│   ├── changelog.md                  # ← LOG #1: What changed
│   └── wow/
│       └── handoff_log.yaml          # ← LOG #3: Who handed off what
│
├── logs/
│   └── thought_trace.md              # ← LOG #2: Why it changed
✅ These are the required paths the GitHub Action is currently looking for.
When a pod creates a patch, it should drop all 3 logs in the same commit, matching these locations.
✍️ We'll add this structure to:
The Wow Guide
The apply_patch.sh script
The Pod SOPs (esp Dev, QA, Research)
