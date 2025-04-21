# 📓 Summary Report Guide

The summary report is a markdown digest generated from the logs after a pod submits a patch. It provides a lightweight way to capture recent work, decisions, and handoffs for project traceability.

---

## 📅 What It Includes

Each summary contains:

### 🧠 Thought Trace Highlights
- The last 10 thought trace entries from `logs/thought_trace.yaml`

### 📒 Changelog Snapshots
- The last 10 patches with:
  - Timestamp
  - Type (`bug`, `feature`, `infra`)
  - Changed files
  - Tags

### 🔁 Handoff Log
- The last 10 pod-to-pod handoffs from `logs/handoff_log.yaml`

---

## 🔧 How to Generate a Summary

This is done automatically when you run:
```bash
python scripts/generate_patch.py --type feature --thought "..." --summary
```

Or you can generate manually with:
```bash
python scripts/generate_summary.py
```

The summary will be saved to:
```
docs/history/summary_<timestamp>.md
```

An entry will also be appended to:
```
docs/SUMMARY.md
```

---

## 🔄 Use Cases
- Team retrospectives and delivery reviews
- Pod handoffs and shared awareness
- Lightweight audit trail for features, bugs, reasoning

Use this to keep everyone on the same page—with almost no extra work. ✨

