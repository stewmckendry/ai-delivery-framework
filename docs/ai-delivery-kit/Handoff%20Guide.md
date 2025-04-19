# 🧠 Handoff & Learning Rituals Guide

Effective handoffs reduce confusion, save time, and build trust across pods. This guide shows how to complete clean handoffs with the `handoff_template.md`.

---

## 🔁 What Is a Pod Handoff?
A pod handoff happens when one pod finishes a phase of work and passes it to another (e.g., dev → qa).

---

## 🔄 Required Artifact
Use `handoff_template.md` to create a short, clear handoff note.

### Save to:
```
docs/handoff/handoff_<feature_or_date>.md
```

### Include in your patch:
- Submit alongside `.diff`
- Mention in `logs/handoff_log.yaml`

---

## ✅ What Makes a Good Handoff?
Include:
- **What changed**: A short summary of what was done
- **What's next**: What the next pod should do, validate, or continue
- **Links to artifacts**: logs, diffs, or summaries
- **Any helpful tips or known caveats**

---

## 👩‍💻 When to Use This
- Finishing a feature
- Passing work mid-sprint
- Wrapping up one-off contributions
- Sharing context for someone picking up a complex issue

---

## ✨ Bonus Tip
Use inline TODO tags (e.g., `# QA_TODO:`) in your code or YAML to flag follow-ups.

---

> Handoffs are about **setting up the next pod to succeed**. A clear pass sets the tone for collaboration.

