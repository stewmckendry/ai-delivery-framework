# 🧱 AI Project Repository Structure & Upkeep Guide

This guide defines the **standard structure** and **upkeep practices** for all AI-native delivery project repositories using the PoD + memory model.

---


## 📁 Directory Structure (Expanded)

```
ai-delivery-framework/
├── task.yaml                      # Central task backlog + metadata
├── .patches/                      # Git-formatted patch files
├── .logs/
│   ├── patches/                   # Patch metadata .json files
│   ├── changelogs/               # Markdown changelogs for each task
│   ├── reasoning/                # Reasoning trace .md files
│   └── feedback/                 # GPT or human review notes
├── prompts/
│   ├── used/                     # Actual prompts used for traceability
│   │   ├── DevPod/
│   │   ├── QAPod/
│   │   ├── ResearchPod/
│   │   └── WoWPod/
│   └── tools/                    # Custom GPT prompt files (e.g. promote_output_file.txt)
├── chatgpt_repo/
│   └── outputs/                  # GPT output zip folder used by patch script
```

---

## 🛠️ Helper Script: Initialize Repo Structure

For onboarding a new repo:

```bash
#!/bin/bash
mkdir -p \
  .patches \
  .logs/patches \
  .logs/changelogs \
  .logs/reasoning \
  .logs/feedback \
  chatgpt_repo/outputs \
  prompts/used/DevPod \
  prompts/used/QAPod \
  prompts/used/ResearchPod \
  prompts/used/WoWPod \
  prompts/tools
```

Save as `scripts/init_repo_structure.sh`


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

---

## ✅ Next Steps

1. **Track Prompts and Reasoning:**
   - Zip final outputs with `metadata.json`, `prompt_used.txt`, and `reasoning_trace.md`
   - Patch process logs prompt + reasoning to `.logs/` and `prompts/used/`

2. **Add `scripts/init_repo_structure.sh`** to project setup guide

3. **Keep docs in sync** with new conventions: changelogs, branches, logs, prompts

4. **Use `memory.yaml`** to index these files for pod + human review

---


This guide evolves with the system — update it as standards or tooling improve!

