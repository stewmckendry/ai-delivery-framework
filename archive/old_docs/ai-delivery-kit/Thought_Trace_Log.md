# 🧠 Thought Trace Log

This file captures structured reasoning behind changes — written by pods or the human lead.

> "We don't just build. We **explain our thinking** as we go."

---

## 📘 How to Use This File

| Aspect | Details |
|--------|---------|
| **When to update** | When proposing a patch or making a decision with LLM reasoning or tradeoffs |
| **Who updates it** | The pod that made the change, or the human lead |
| **How it's used** | Referenced in GitHub PRs, changelogs, and post-sprint reviews |
| **Required in PRs** | ✅ Yes – recommended for any non-trivial patch |

---

## 📜 Format
Each entry is linked to a feature, file, or PR. Include:
- `Feature:` or `Patch:` (ID or filename)
- `Author:` (which pod or "human")
- `Date:`
- `Reasoning:` What logic, constraints, or insight drove the change?
- Optional: `Linked Files:` or `Changelog Ref:`

---

## Example Entry

---
### Patch: gpt_patch_f4.3.diff
**Author:** dev_pod  
**Date:** 2025-04-22

**Reasoning:**
> User symptom data was often missing. We added a fallback response in `guidance_generator.py` to handle empty input and guide users to complete symptom checklist. This avoids hallucinated guidance from the LLM and aligns with QA-pod feedback.

**Linked Files:**  
- `src/models/guidance_generator.py`  
- `data/prompts/guidance_prompt.yaml`

**Changelog Ref:** Sprint 2 – F4.3

---

Entries are added by pods or the human at time of patch creation.
All PRs should ideally reference at least one trace entry.

