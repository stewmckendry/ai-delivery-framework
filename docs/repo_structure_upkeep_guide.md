# 🧱 AI Project Repository Structure & Upkeep Guide

This guide defines the **standard structure** and **upkeep practices** for all AI-native delivery project repositories using the PoD + memory model.

---

## 📁 Directory Structure

```
ai-concussion-agent/
├── README.md                      # Project overview and quickstart
├── memory.yaml                   # Index of key files for PoDs and humans
├── project_manifest.yaml         # Overview of key stages and configuration
├── feature_backlog.yaml          # Active features and backlog items
│
├── docs/                         # All documentation files
│   ├── ai_delivery_operating_system.md
│   ├── ai_native_progress.md
│   ├── ai_native_generate_patch.md
│   └── ai-delivery-kit/
│       └── POD_SOPs.md
│
├── scripts/                      # System automation scripts
│   ├── generate_patch.py
│   ├── create_pr_from_patch.sh
│   ├── update_memory.py          # (to be built)
│   ├── check_repo_structure.py   # (to be built)
│   └── other_helpers.py
│
├── patches/                      # PoD-generated .diff patches
├── logs/                         # Evaluation logs and traces
├── src/                          # Application code
│   ├── client/                   # Streamlit front-end
│   ├── server/                   # FastAPI backend
│   ├── models/                   # LLM, validation, and protocol logic
│   └── utils/                    # Shared utilities
├── test/                         # Unit and integration tests
├── data/                         # Sample inputs (YAMLs, reference docs)
├── outputs/                      # Generated reports (JSON, markdown, PDF)
├── archive/                      # Deprecated or old content for reference
└── .github/
    └── workflows/                # GitHub Actions, CI/CD pipelines
```

---

## 🧠 memory.yaml Guidelines

- **All important files** (docs, scripts, SOPs, outputs) must be indexed.
- Format:

```yaml
memory:
  pod_sops: docs/ai-delivery-kit/POD_SOPs.md
  generate_patch:
    doc: docs/ai_native_generate_patch.md
    script: scripts/generate_patch.py
  pr_script: scripts/create_pr_from_patch.sh
  ai_os_guide: docs/ai_delivery_operating_system.md
  progress: docs/ai_native_progress.md
```

---

## 🛠️ Required Scripts

| Script | Purpose |
|--------|---------|
| `scripts/generate_patch.py` | Create .diff patch for PoD outputs |
| `scripts/create_pr_from_patch.sh` | Promote patch to feature branch and open PR |
| `scripts/update_memory.py` | Auto-update memory.yaml by scanning docs/scripts (to be built) |
| `scripts/check_repo_structure.py` | Enforce repo hygiene and structure (to be built) |

---

## 📄 GitHub Contribution Templates

### `.github/PULL_REQUEST_TEMPLATE.md`

```markdown
### 📌 Summary
Brief description of what this PR does.

### 📂 Files Added or Modified
- [ ] I placed new files in the correct folder (e.g. docs/, scripts/, src/)
- [ ] I updated `memory.yaml` for key docs/scripts

### 🧠 Notes for Reviewers
(Optional) Anything to know when reviewing.
```

---

## 🚹 Upkeep Tips

- Archive rather than delete: move deprecated content into `/archive/`
- Use `git add -u` to capture deletions and renames properly
- Use consistent naming: kebab-case or snake_case, no spaces
- Validate repo regularly with `check_repo_structure.py`
- Keep `memory.yaml` in sync with real file structure

---

## ✅ Next Steps

1. **Build missing scripts:**
   - `scripts/update_memory.py`
   - `scripts/check_repo_structure.py`

2. **Update `memory.yaml`** to reflect all critical files across `docs/` and `scripts/`

3. **Add PR enforcement**:
   - Create `.github/PULL_REQUEST_TEMPLATE.md`
   - Optional: add GitHub Actions to check memory.yaml consistency

4. **Document conventions** in `CONTRIBUTING.md` (or in docs/ai-delivery-kit)

5. **Apply this standard** across future PoD projects

---

This guide evolves with the system — update it as standards or tooling improve!

