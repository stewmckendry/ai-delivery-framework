# 📒 Changelog – AI-Native Delivery

This file records every meaningful change to the system, app, or reasoning flow — made by humans or pods.

> A changelog is not just what changed — it's **why** and **what it unlocks**.

---

## 📘 How to Use This File

| Aspect | Details |
|--------|---------|
| **When to update** | Any time a patch, feature, or file is added, changed, or removed |
| **Who updates it** | The pod proposing the change or the human lead |
| **How it’s used** | Referenced in GitHub PR bodies, sprint logs, release notes |
| **Required in PRs** | ✅ Yes – each PR should map to a Sprint entry |

---

## 📜 Format
Each entry should follow this structure:

### Sprint <Number> – <Date Range>

#### ✨ Added
- `<filename>` – what was added and why

#### 🐛 Fixed
- `<issue>` – what was fixed and what it affects

#### 🔁 Changed
- `<behavior>` – what changed and why

#### 🧠 Reasoning
Brief note from pod or human on what motivated this change. Optional link to `thought_trace.md` entry.

---

## Example

### Sprint 2 – April 22–29

#### ✨ Added
- `guidance_generator.py` in `src/models/` – initial symptom-to-guidance logic
- `guidance_prompt.yaml` in `data/prompts/` – prompt template for F4.3

#### 🐛 Fixed
- N/A

#### 🔁 Changed
- N/A

#### 🧠 Reasoning
Needed for MVP delivery of return-to-play advice. Prompt designed for interpretability.

---

All pods and the human lead contribute to this file. One change = one entry. Append only. ✅

