# 🚀 New Project Onboarding Guide – AI Delivery Kit

Welcome to your first AI-native delivery project. This guide walks you through how to get started using the delivery kit.

---

## ✅ What You’ll Get
- Pre-built folder structure
- Scripts for patch, log, and summary generation
- Pod SOPs and collaboration rules
- A structured system for velocity tracking and traceability

---

## 🛠️ Setup Instructions

### 1. Clone the Starter Repo
```bash
git clone https://github.com/YOUR_ORG/ai-delivery-kit.git your-project
cd your-project
```

### 2. Run the Initialization Script
```bash
python scripts/wow_init.py
```
This sets up:
- `.patches/`, `.metrics/`, `logs/`, `docs/`, `docs/handoff/`, `docs/history/`
- YAML log files (empty but ready to append)

### 3. Review Pod SOPs
Each team member should read:
```bash
docs/POD_SOPs.md
docs/POD_CONTRIBUTING_Guide.md
```

---

## 🧠 Pod Activation
Each pod (e.g. dev, qa, research, wow) should:
- Review their responsibilities in `POD_SOPs.md`
- Start using `scripts/generate_patch.py` to contribute
- Follow the log rituals (thought trace, changelog, handoff if needed)

---

## 📌 Additional Setup (Optional)
- Add this repo as a GitHub template
- Configure `generate_summary.py` as a scheduled GitHub Action
- Add `.env` with any project-specific vars or keys
- Pre-load project-specific specs into `docs/specs/`

---

## 🔄 Onboarding Checklist

- [ ] Cloned repo and renamed project folder
- [ ] Ran `wow_init.py`
- [ ] Assigned pods to team members
- [ ] Shared `POD_SOPs.md` and walkthrough
- [ ] First backlog item defined in `feature_backlog.yaml`

---

> This isn’t just a repo. It’s your system for moving fast, together, with traceable AI-native delivery.

Let’s build!

