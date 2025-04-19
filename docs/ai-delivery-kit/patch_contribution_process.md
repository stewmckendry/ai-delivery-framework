# 🧠 AI-Native Patch Contribution Process

This document explains how each component in the AI-native delivery system works individually and together during the patch contribution workflow.

---

## 🔧 Individual Components

### 1. `generate_patch.py`
**Purpose:** Creates a `.diff` patch file and logs from staged changes.

**Key functions:**
- `git diff --cached`: gets changes you've staged with `git add`
- Generates a patch file in `.patches/`
- Appends metadata to:
  - `.logs/thought_trace.yaml`
  - `.logs/changelog.yaml`
  - `.logs/handoff_log.yaml`
- Optional flags:
  - `--type`: label for patch (e.g. feature, bug, infra)
  - `--thought`: reasoning behind the change
  - `--autopromote`: triggers the promotion script (see below)

**Typical usage:**
```bash
git add test_file.md
python scripts/generate_patch.py --type feature --thought "Add test file" --autopromote
```

---

### 2. `create_pr_from_patch.sh`
**Purpose:** Promotes a patch to a Git branch and opens a PR (via GitHub CLI)

**Steps:**
- Finds `.patches/*.diff`
- Creates new branch: `chatgpt/auto/<patch_id>`
- Applies patch using `patch -p1`
- Commits supporting files (e.g. logs)
- Pushes branch
- Runs `gh pr create` (if GitHub CLI is available)

**You can also run this directly:**
```bash
bash scripts/create_pr_from_patch.sh
```

---

### 3. `patch_promoter.py` *(Planned)*
**Purpose:** Moves patch and logs from `.patches/queue/` to proper folders, commits, and pushes.

**When used:**
- After ChatGPT generates `.diff` + logs and you download them
- You run this script to finalize their promotion to GitHub

---

### 4. `download_patch_from_chatgpt.py` *(Planned)*
**Purpose:** A utility script for humans to quickly organize files downloaded from ChatGPT’s sandbox.

**Functionality:**
- Accepts downloaded `.diff`, `.yaml`, or `.md` files
- Moves them into project folders:
  - `.patches/queue/` for patch files
  - `.logs/` for changelog, thought trace, handoff logs
- May include optional validation (e.g., check patch format)

**When used:**
- After a pod announces a patch is ready and provides download links or file paths

---

### 5. GitHub Action: `apply_patch_enhanced.yaml`
**Purpose:**
- Triggered by a `push` to `.patches/`
- Applies patch and opens a PR automatically

**Steps:**
- Checks out code
- Reads `.patches/*.diff`
- Creates a branch
- Applies the patch
- Commits and pushes
- Opens a PR (if not already done)

---

## 🔁 How They Work Together

### Full Process Flow

1. **ChatGPT (or you) modify files**
2. `git add` to stage changes
3. Run:
```bash
python scripts/generate_patch.py --type feature --thought "F2.1 - Add parser" --autopromote
```
  - Creates `.diff` and logs
  - Triggers `create_pr_from_patch.sh`

4. `create_pr_from_patch.sh`:
  - Applies patch to new branch
  - Commits logs and files
  - Pushes to GitHub
  - Opens PR via GitHub CLI (if configured)

5. **OR** if `autopromote` is not used:
  - You can manually run `patch_promoter.py` to push files

6. **GitHub Action** (if configured) detects push:
  - Applies patch in cloud
  - Opens PR with logs and trace

7. (Planned) After ChatGPT notifies human of patch files:
  - Run `download_patch_from_chatgpt.py` to organize and place files
  - Then promote using `patch_promoter.py`

---

## 📋 Human / ChatGPT Responsibilities

> 🔄 Note: `generate_patch.py` is designed to be triggered by **ChatGPT** (when integrated in agent workflows), but it is typically **run by the human** today in local development. In AI-native delivery, ChatGPT can suggest exactly what to stage and how to structure the patch — but the human runs the script until full CLI/agent integration is in place.

| Step | Performed By | Tool |
|------|--------------|------|
| Modify code | ChatGPT or Human | Any editor |
| Stage files | Human | `git add` |
| Generate patch + logs | ChatGPT (via script) | `generate_patch.py` |
| Move patch from sandbox | Human | Manual or `download_patch_from_chatgpt.py` (planned) |
| Promote patch to repo | Human | `patch_promoter.py` or `create_pr_from_patch.sh` |
| Push to GitHub | Human | `git push` or via script |
| Review and merge PR | Human Lead | GitHub UI |

---

## 🛠️ Notes

- A `.diff` file (patch) includes all changes made to a file — including the full contents of new files.
  - If a new file is created, the `.diff` will contain `new file mode`, `index`, and all added lines prefixed with `+`
  - This means that **you do not need to push the new file itself** — the patch will recreate it wherever applied


- `generate_patch.py` is the starting point of the contribution pipeline
- Use `--autopromote` if you want the system to handle PR creation directly
- Logs are critical for traceability — always commit `.logs/` together with patches
- GitHub Actions and Apps **should not conflict** — pick one as your promotion mechanism

---

## 📘 Glossary of DevOps Terms

| Term | Definition |
|------|------------|
| **Patch** | A set of code changes, usually in `.diff` format, that modifies source files |
| **Diff (.diff)** | A file that shows the differences between two sets of files (used to apply code changes) |
| **Commit** | A saved snapshot of changes to your codebase in Git |
| **Branch** | A parallel version of the codebase used for isolated development |
| **Push** | Upload your local commits to the GitHub remote repository |
| **PR (Pull Request)** | A request to merge one branch (often with new changes) into another |
| **Staging Area** | The Git step between changing a file and committing it; used by `git add` |
| **GitHub Action** | A CI/CD automation task triggered by GitHub repo events (like `push`) |
| **GitHub CLI (`gh`)** | A command-line tool for interacting with GitHub (e.g., creating PRs) |
| **Webhook** | A way GitHub notifies external services when something happens (like a push) |
| **Promotion** | The act of taking work from sandbox/queue to a Git-tracked branch and PR |

Let this document guide all pods and contributors through patch-based development.
