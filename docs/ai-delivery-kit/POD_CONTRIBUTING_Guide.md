# ✍️ CONTRIBUTING.md – AI-Native Delivery

Welcome to our human + AI delivery system! This guide defines how each pod (and human) contributes code, content, and structured reasoning artifacts in a traceable, collaborative way.

---

## 🧠 General Guidelines

- All meaningful contributions — whether code, markdown, YAML, JSON, prompts, or protocols — are submitted via `.diff` patch files into `.patches/`
- This includes **features, tests, prompts, documentation, structured flows, and specs**
- Each patch must include:
  - 📒 `logs/changelog.yaml` entry – what changed and why
  - 🧠 `logs/thought_trace.yaml` entry – how it was reasoned
  - 🔁 `logs/handoff_log.yaml` entry – **only if** the work is being handed off to another pod
- GitHub Actions will auto-apply the patch, create a feature branch, and open a pull request with these logs included

---

## 🧠 Folder Structure

| Folder | Purpose |
|--------|---------|
| `.patches/` | Patch files dropped by pods (e.g. `gpt_patch_f3.1_dev.diff`) |
| `docs/` | Changelog, specs, markdown outputs, delivery SOPs |
| `logs/` | Reasoning traces for decisions or logic |
| `scripts/` | Tools for automation (e.g. `generate_patch.py`) |
| `.github/workflows/` | GitHub Action to apply patches + open PRs |

---

## 📦 Patch Naming Convention

- Format: `gpt_patch_<feature_id>_<pod_type>.diff`
- Example: `gpt_patch_f4.3_dev.diff`
- One patch per feature, fix, or deliverable (code, content, YAML, or flow)

---

## 📋 Log Files – Format and Behavior

| Log File | Type | Format | Behavior |
|----------|------|--------|----------|
| `changelog.yaml` | Append-only | YAML | Shared master file — 1 entry per change or sprint |
| `thought_trace.yaml` | Append-only | YAML | Shared master — entries added per patch |
| `handoff_log.yaml` | Append-only | YAML | Shared master — each handoff is a new item if a file is passed to another pod |

> These are not overwritten or per-feature files. The GitHub Action reads the latest entries per patch and includes them in the PR.

**To view recent entries**: scroll to the bottom of each file (most recent entries are always added last).

If a change does **not involve a handoff** (e.g., a dev pod updates a YAML spec but no other pod is involved), the contributor **only needs to update `changelog.yaml` and `thought_trace.yaml`.** The `handoff_log.yaml` can be left unchanged.

---

## 🤖 Pod Responsibilities

### `dev_pod`
- Writes or modifies code, prompts, or structured YAML specs
- Uses `generate_patch.py` before submission
- Appends changelog and thought trace entries

### `qa_pod`
- Creates test plans, validation cases, and regression probes
- Documents test logic and risk reasoning in `thought_trace.yaml`

### `research_pod`
- Investigates external references, extracts structured data
- Produces YAML specs, markdown briefs, or prompt suggestions
- Explains synthesis logic and references in `thought_trace.yaml`

### `wow_pod`
- Improves delivery model, tools, or process rituals
- Maintains docs under `docs/wow/` and pod SOPs

---

## ✅ Submission Checklist

- [x] `.diff` file dropped into `.patches/`
- [x] `logs/changelog.yaml` updated (append at bottom)
- [x] `logs/thought_trace.yaml` updated (append at bottom)
- [x] `logs/handoff_log.yaml` updated **only if files are handed off to another pod**
- [x] Pull request is created by GitHub Action and includes all logs

---

# 🛠 Using `generate_patch.py` – Patch Submission Tooling

All pods should use the `generate_patch.py` script to generate, validate, and log their contributions in a traceable way.

This script:
- Creates a `.diff` patch file from staged Git changes
- Validates that `tests/` and `docs/` are updated where expected
- Appends entries to:
  - `logs/changelog.yaml`
  - `logs/thought_trace.yaml`
  - `logs/handoff_log.yaml` (if a handoff is declared)

### 📌 Example Usage
```bash
python scripts/generate_patch.py \
  --type feature \
  --thought "Added validation logic to enforce test+doc updates" \
  --from-pod dev \
  --to-pod qa \
  --update-metrics
```

### 🎛️ Command Line Options

| Flag | Description |
|------|-------------|
| `--type` | Required tag for the patch type: `bug`, `feature`, or `infra` |
| `--thought` | Optional reasoning note that gets appended to `thought_trace.yaml` |
| `--from-pod` | Pod initiating the handoff (defaults to `dev`) |
| `--to-pod` | Target pod for handoff (defaults to `qa`) |
| `--update-metrics` | Triggers downstream metrics update logic (stubbed for now) |
| `--skip-log` | Skips saving the patch to `.patches/` (useful for dry runs) |

### ✅ Built-In Safeguards
- Runs `validate_patch.py` before writing the patch
- Warns if `tests` or `docs` folders were not touched
- Suggests PR tags based on changed files and patch type

> 📌 Tip: Always stage your changes (`git add`) before running the script.

---

## 🧪 Pod-Specific Cheat Sheet

### Dev Pod
```bash
python scripts/generate_patch.py \
  --type feature \
  --thought "Built new logic for YAML loader" \
  --from-pod dev \
  --to-pod qa \
  --update-metrics
```

### QA Pod
```bash
python scripts/generate_patch.py \
  --type bug \
  --thought "Tested logic for edge case handling" \
  --from-pod qa \
  --to-pod dev \
  --update-metrics
```

### Research Pod
```bash
python scripts/generate_patch.py \
  --type feature \
  --thought "Added CDC concussion symptom list to YAML spec" \
  --from-pod research \
  --to-pod dev \
  --update-metrics
```

### WoW Pod
```bash
python scripts/generate_patch.py \
  --type infra \
  --thought "Refined pod coordination workflow" \
  --from-pod wow \
  --to-pod dev \
  --update-metrics
```

