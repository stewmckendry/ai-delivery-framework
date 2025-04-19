# 🔁 Handoff Template

> Use this when transitioning work from one pod to another. Submit this as `docs/handoff/handoff_<feature_or_date>.md`.

---

## 📅 Handoff Date
YYYY-MM-DD

## 🌍 Pod Handoff
**From Pod:** `dev`
**To Pod:** `qa`

## 🔄 What Changed
_Describe what was delivered in this patch or sprint. Be concise but clear._

- Feature XYZ was implemented
- YAML spec updated for condition handling
- Patch includes test scaffolding

## 🛠 What's Next
_Summarize what the next pod should do or watch for._

- Validate that edge cases are covered
- Confirm symptom extraction aligns with spec
- Add retry logic if missing

## 📒 Related Artifacts
_Include paths to relevant logs, patches, summaries._

- `logs/changelog.yaml`
- `logs/thought_trace.yaml`
- `logs/handoff_log.yaml`
- `docs/history/summary_<date>.md`

## ✨ Tips or Warnings
_Anything that would help someone pick this up smoothly._

- Retry logic may fail on empty strings
- TODOs marked inline with `# QA_TODO:`

---

> Submit this file along with your patch if handing off responsibility to another pod.

