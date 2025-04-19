# 🔁 Handoff Log – Pod Collaboration

This YAML file tracks file-level handoffs between pods and/or the human lead.

> "Every file handed from one pod to another is a baton in the race. This log is the relay map."

---

## 📘 How to Use This File

- **When to update:** Every time a pod hands off one or more files to another pod (e.g., Dev to QA).
- **Who updates it:** The pod initiating the handoff (or human lead, if coordinating).
- **How it’s used:**
  - Enables traceability of inter-pod collaboration
  - Used by GitHub Action to enrich pull request metadata
  - Supports metrics (handoff frequency, cycle time)
- **Should it be referenced in PRs?** ✅ Yes – patches that represent collaboration across pods should log a handoff

---

## 🧭 Format
Each handoff should include:
- `from:` (pod or "human")
- `to:` (pod or "human")
- `date:` (ISO format preferred)
- `files:` (list of relative paths)
- `reason:` (what this handoff enables)
- Optional: `related_patch:` or `feature:`

---

## Example

```yaml
handoffs:
  - from: dev_pod
    to: qa_pod
    date: 2025-04-22
    files:
      - src/models/guidance_generator.py
      - data/prompts/guidance_prompt.yaml
    reason: "Ready for QA validation of fallback logic"
    related_patch: gpt_patch_f4.3.diff

  - from: research_pod
    to: dev_pod
    date: 2025-04-20
    files:
      - data/protocols/return_to_play.yaml
    reason: "Structured RTP stages extracted from Canadian guideline"
    feature: F4.1
```

---

This log enables traceability of inter-pod collaboration and justifies transitions.
One row per handoff. Append only. ✅

