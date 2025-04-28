# 🌿 AI-Native Branching Spec for Pod-Driven Delivery

## ✅ Overview
This branching strategy supports structured, low-friction collaboration across AI delivery pods. It ensures that each task is tied to a predictable Git branch based on its category (Discovery, Dev, QA, etc.), reducing clutter and simplifying automation.

---

## 🔢 Branch Naming Convention
Branches follow this format:

```
chatgpt/auto/<category>/<task_id>
```

Where:
- `<category>` is the task category (`discovery`, `dev`, `e2e`, `cutover`, `fix`)
- `<task_id>` is the unique task ID from `task.yaml`

### 🔍 Examples
```
chatgpt/auto/discovery/1.1_capture_goals
chatgpt/auto/dev/2.3_build_feature_prompting
chatgpt/auto/e2e/3.1_validate_flow
chatgpt/auto/cutover/4.2_deploy_to_prod
```

---

## 📁 Source of Truth
The branch name is derived from `task.yaml`, using:

```yaml
tasks:
  2.3_build_feature_prompting:
    category: dev
    ...
```

---

## 🛠 Automation Support

### `generate_patch_from_output.sh`
- Extracts `task_id` and `category` from `metadata.json` and `task.yaml`
- Sets `BRANCH_NAME` to `chatgpt/auto/<category>/<task_id>`
- Writes `branch_name` into the final `.json` patch metadata

### `create_pr_from_patch.sh`
- Reads `branch_name` from the `.json` metadata
- Uses it to:
  - Checkout or create the correct branch
  - Apply patch and commit
  - Push and open PR

---

## ✅ Branch Lifecycle Rules
- One branch per task (even across multiple patches)
- Auto-delete branches after merge (GitHub setting)
- Local cleanup via `scripts/prune_old_branches.sh`

---

## 🧹 Cleanup Script
```bash
bash scripts/prune_old_branches.sh
```
- Prunes stale local and remote branches under `chatgpt/auto/*`
- Asks for confirmation before deletion

---

## 📝 PR Naming Convention
- PR title is derived from `summary` in metadata
- Optionally prefixed by pod label (e.g. `[DevPod]`)
- All PRs trace back to a task ID

---

## 🔄 Future Enhancements
- GitHub Action to validate branch names pre-push
- Pod-to-branch mapping table
- PR labels based on `category`

