# 🧠 AI Concussion Agent – Pod Contribution Guide

Welcome to the team! Here's how ChatGPT pods contribute to this project using the AI Delivery Kit.

---

## 📦 One-Time Setup

```bash
git clone https://github.com/stewmckendry/ai-delivery-framework.git
cd ai-delivery-framework
./scripts/setup_ai_delivery.sh
```

Ensure you have:
- `gh` GitHub CLI installed and authenticated
- Python installed

---

## 🚀 Submitting a Patch

1. Stage your work:
   ```bash
   git add path/to/your/files
   ```

2. Generate a patch:
   ```bash
   python scripts/generate_patch.py --type feature --thought "Modularized parser"
   ```

3. Commit and open a PR:
   ```bash
   git commit -m "F1.2: Parser refactor from dev_pod"
   gh pr create --title "F1.2 Parser Refactor" --body "Patch for feature F1.2 from dev_pod"
   ```

---

## 🧠 Logs + Trace

- Patches are saved to `logs/patches/`
- Thought trace → `logs/thought_trace.yaml`
- Metrics tracked in `logs/metrics.yaml`
- PRs are labeled by type automatically

---

Want to view patches, track delivery, or inspect thoughts? Check the `/logs/` folder or use `generate_summary.py`.

You're now AI-native. Let's build. 🚀

