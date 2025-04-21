# 🛠️ Delivery Kit Maintenance Process

As the AI Delivery Kit gets used in more projects, we need clear processes for updating it responsibly — without breaking dependent pods.

---

## 👥 Who Maintains the Kit?
The **WoW pod** owns the AI Delivery Kit as a living system.
It acts as the steward of platform quality, velocity, and improvement across all projects.

---

## 📍 What This Covers
- Updating SOPs, scripts, templates
- Accepting suggestions from project pods
- Keeping docs in sync with behavior

---

## ♻️ Change Types

| Type | Description |
|------|-------------|
| `fix` | Correct typos, bugs in scripts, or doc mismatches |
| `feature` | Add new scripts, log types, guides |
| `refactor` | Reorganize layout, merge files, simplify flow |
| `infra` | Add CI/CD, metrics, or automation helpers |

---

## ✅ Change Flow

1. Pod opens patch with `generate_patch.py`
2. Use `--type` and `--from-pod wow` to flag intent
3. Append to `logs/changelog.yaml`, `thought_trace.yaml`
4. Tag PR as `infra`, `wow`, `doc` as needed

---

## 🧪 Testing Guidelines
- All script changes should run locally with:
```bash
python scripts/wow_init.py
python scripts/generate_patch.py --help
```
- Markdown previews should be tested in a GitHub markdown renderer

---

## 📖 Canonical Files
- `README.md`
- `POD_SOPs.md`
- `generate_patch.py`
- `wow_init.py`

Keep these synced. If one changes, update references across others.

---

## 📬 Feedback & Contribution Process
- **There are two ways project pods can help improve the Delivery Kit:**

### 1. ✅ Minor Suggestions → Feedback Patch
- Submit `PATCH: WOW_FEEDBACK.md` inside your own project repo
- Include:
  - Suggestions
  - Missing docs or templates
  - Confusing SOP or script usage
- The `wow` pod will triage feedback **every Friday** and apply improvements to the central kit

### 2. 🛠 Major Changes → Direct PR to Delivery Kit
- If you want to directly fix or enhance the kit (e.g. `generate_patch.py`, `wow_init.py`, docs):
  - Clone or fork `ai-native-delivery` repository
  - Use `generate_patch.py --from-pod wow` to structure your changes
  - Submit a Pull Request with `infra` or `wow` tag
- A core member of the WoW pod will review and merge your patch
- Include suggestions, issues, confusing workflows
- WoW pod triages these every Friday

---

## 🧭 Kit vs. Project Customization

### 🏛️ Core Delivery Kit (Shared)
The main `ai-native-delivery` repo is maintained by the WoW pod and should serve as the **canonical source** for:
- Scripts: `generate_patch.py`, `wow_init.py`, `generate_summary.py`
- SOPs and rituals: `POD_SOPs.md`, `POD_CONTRIBUTING_Guide.md`
- Templates: prompt specs, test plans, handoff notes

### 🧩 Per-Project Customization
Each project **clones the delivery kit** as a starting point and may tailor it to their workflows:
- Modify SOPs to reflect client/team context
- Add domain-specific templates or test cases
- Extend scripts as needed (but consider contributing reusable changes back!)

> If a project diverges significantly, document why and flag to WoW pod for potential system-wide improvements.

---

## 🔄 Keeping Projects in Sync

To help individual projects stay up to date with improvements in the Delivery Kit:

### 🧰 Add a Sync Script to Each Project
Include this in `scripts/sync_with_upstream.py`:
```python
import os
from subprocess import run

# Assumes delivery kit remote is set as 'upstream'
run(["git", "fetch", "upstream"])
run(["git", "checkout", "main"])
run(["git", "merge", "upstream/main"])
print("[OK] Synced with upstream Delivery Kit")
```

### 📦 Setup Upstream Remote
Projects should add the main kit as a remote:
```bash
git remote add upstream https://github.com/YOUR_ORG/ai-native-delivery.git
```

### 🔔 When to Sync
- Monthly cadence
- After major PR merges to Delivery Kit
- When adding new pods, rituals, or logs

---

## 🪡 Recommendations
- Review logs from active projects monthly
- Auto-run link/reference checkers on markdown docs
- Bake feedback insights into `docs/POD_SOPs.md` and generator scripts

> The Delivery Kit is our platform. If we tend it well, it gets stronger with every patch.

