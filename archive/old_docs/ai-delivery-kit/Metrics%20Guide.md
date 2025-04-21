# 📊 Metrics Guide – AI-Native Delivery System

This guide explains how delivery metrics are collected, tracked, and used across pods to drive visibility, quality, and improvement.

---

## 🎯 Purpose of Metrics

Metrics help us:
- Track work velocity and pod contribution
- Surface quality trends (e.g. test coverage, bugs caught)
- Monitor feature burn down and delivery progress
- Enable reflective retrospectives
- Keep AI-native delivery accountable and scalable

---

## 📂 Where Metrics Live

| File | Purpose |
|------|---------|
| `.metrics/metrics.yaml` | Time-stamped snapshots of patch and pod activity |
| `.metrics/velocity.md` | Current patch velocity and contributors |
| `.metrics/burndown.md` | Outstanding vs. delivered feature map |
| `.metrics/retrospective.md` | Insights and reflections after each sprint |

---

## 📏 Metrics Tracked

| Type | Description |
|------|-------------|
| Patch Frequency | # of patches submitted per pod |
| Feature Coverage | Unique features touched per pod |
| PR Merge Rate | % of patches merged vs. proposed |
| Handoff Count | # of inter-pod handoffs (from YAML log) |
| Reasoning Richness | % of patches with thought trace entries |
| Retrospective Notes | Manually added per sprint for context |

---

## ⚙️ How Metrics Are Collected

1. Run `metrics_tracker.py` to scan `.patches/` and generate pod stats
2. Track handoffs from `handoff_log.yaml`
3. Pull PR results and merge status via GitHub API (coming soon)
4. Append summaries to markdown reports

---

## ✅ Pod & Admin Usage

### For Pods:
- View your contribution stats in `velocity.md`
- Review burndown to see pending or stale features
- Add reflections to `retrospective.md` when prompted by the WoW Pod

### For Admin (Human Lead):
- Use `metrics.yaml` for weekly delivery snapshot
- Use burndown chart to steer planning
- Review changelog + thought_trace to calibrate quality

---

## 🧠 Reflect, Don't Just Count

Metrics are not for pressure — they're for learning. We measure so we can:
- Improve how we work
- Balance speed and quality
- Build trust between pods and delivery

Use this guide alongside GitHub insights and pod retros to keep growing.

Let’s measure what matters. 🚀