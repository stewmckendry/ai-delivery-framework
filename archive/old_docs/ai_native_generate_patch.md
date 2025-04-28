# 📦 Patch Contribution Process

This guide explains the end-to-end process for contributing patches in an AI-native delivery pipeline using `generate_patch.py`, GitHub Actions, and Pull Requests. It supports both **ChatGPT Pods** and **Human Leads**.

---

## 🧠 Purpose
To enable seamless, automated contribution of code, content, and logs by ChatGPT pods, with human review and GitHub PR workflows.

---

## 👥 Roles

### 🔹 ChatGPT Pod (e.g. DevPod, QAPod)
- Creates outputs for a task (e.g. code, tests, research)
- Runs `generate_patch.py` to generate a `.diff` file
- Specifies where outputs should go in repo (e.g. `src/`, `test/`, `docs/`)
- Notifies the Human Lead when the patch is ready

### 🔹 Human Lead
- Downloads `.diff` and outputs from ChatGPT
- Runs `copy_patch_to_repo.py` (TBD) to place files in `.patches/`
- Pushes `.diff` to GitHub repo to trigger patch promotion
- Reviews PR and merges if correct
- Can push direct changes to `main` (see below)

---

## 🔄 Contribution Flow

### 1. Pod Generates Patch
```bash
python scripts/generate_patch.py --type feature --thought "Add symptom parser" --autopromote
```
- Saves output diff to `.patches/patch_<timestamp>.diff`
- Applies patch to clean feature branch: `chatgpt/auto/patch_<timestamp>`
- Opens a GitHub PR via CLI if local

### 2. Human Moves Files to Repo
> TBD: Will run `scripts/copy_patch_to_repo.py` to download from ChatGPT and stage in `.patches/`

### 3. GitHub Action Auto-PR
`.github/workflows/promote_patch.yaml` watches `.patches/*.diff`
- Applies patch using `scripts/create_pr_from_patch.sh`
- Opens PR to `main`

### 4. Human Reviews + Merges
- Opens the PR (title: "📦 Patch: patch_<timestamp>")
- Clicks **Merge** if correct

---

## 👤 Human Contributor FAQ

### ✅ Can I push directly to `main`?
Yes! As long as you do **not** touch the `.patches/` folder, you can safely:

```bash
git add src/some_code.py
git commit -m "Update feature"
git push origin main
```

This does **not** trigger the patch promotion workflow.

### ❌ When does GitHub Action run?
Only if you push a `.diff` to the `.patches/` folder. For example:
```bash
git add .patches/patch_20250420_130000.diff
```
This will trigger `promote_patch.yaml` and try to auto-apply the patch + PR.

---

## 🛠️ Scripts Overview

### `scripts/generate_patch.py`
- Auto-generates and saves diff
- Applies patch and commits
- Opens PR (optional)

### `scripts/create_pr_from_patch.sh`
- Used by GitHub Action or manually
- Detects `.diff`, applies it, opens PR
- Handles:
  - Branch naming
  - Stash/restore local changes
  - Patch cleanup after apply

### `scripts/resolve_merge_conflicts.sh`
- Auto-cleans known merge conflict scenarios
- Useful when a file is both staged and patched

---

## 🧪 Local Dev Tips

### View All Patch Branches
```bash
git branch | grep chatgpt/auto
```

### Delete Old Patch Branches
```bash
git branch -D chatgpt/auto/patch_<timestamp>
```

### Recover from Merge Conflicts
```bash
bash scripts/resolve_merge_conflicts.sh
```

---

## 🧠 Common Gotchas
- ❌ **Don't `git add` files before running `generate_patch.py`** → causes merge conflict
- ✅ Let the patch generator handle staging/committing
- ❌ Don't commit ChatGPT files manually — use patches
- ✅ Human can push regular changes to `main` (just avoid `.patches/`)

---

## ✅ Next Steps
- [ ] Finalize `copy_patch_to_repo.py` for human patch uploads
- [ ] Enhance `generate_patch.py` with path validation + duplicate detection
- [ ] Enable metadata tagging of patches by Pod and purpose
- [ ] Add PoD-type-specific folders or manifest to organize output

---

## 📚 Glossary

| Term       | Description |
|------------|-------------|
| Patch      | A `.diff` file with changes to be applied to the repo |
| Branch     | A separate line of code history (e.g. `chatgpt/auto/patch_xxx`) |
| Commit     | A recorded snapshot of changes |
| Push       | Upload local commits to GitHub |
| PR         | Pull Request — propose changes from a branch into `main` |
| PoD        | ChatGPT agent for a delivery task (Dev, QA, Research, etc) |

---

## 📌 Reference
- [`scripts/generate_patch.py`](https://github.com/stewmckendry/ai-delivery-framework/blob/main/scripts/generate_patch.py)
- [`scripts/create_pr_from_patch.sh`](https://github.com/stewmckendry/ai-delivery-framework/blob/main/scripts/create_pr_from_patch.sh)
- [Workflow YAML](https://github.com/stewmckendry/ai-delivery-framework/blob/main/.github/workflows/promote_patch.yaml)
