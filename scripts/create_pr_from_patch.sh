#!/bin/bash
set -e

# Load patch file
PATCH_FILE="${TRIGGERED_PATCH:-$(ls -t .patches/*.diff | head -n 1)}"
PATCH_NAME=$(basename "$PATCH_FILE")
PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
PATCH_JSON="${LOG_DIR}/${PATCH_NAME%.diff}.json"

echo "📎 Using triggered patch file: $PATCH_FILE"

# Step 0: Stash any current work to avoid overwriting
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Stashing uncommitted changes..."
  git stash push -m "pre-patch-stash-$(date +%s)"
  STASHED=1
else
  STASHED=0
fi

# Step 1: Extract metadata
TASK_ID=$(jq -r .task_id "$PATCH_JSON")
SUMMARY=$(jq -r .summary "$PATCH_JSON")
BRANCH_NAME="chatgpt/auto/${PATCH_NAME%.diff}"

# Step 2: Get latest main branch from remote git, then checkout branch for patch (create new one if it doesn't exist)
echo "🔄 Updating main before creating patch branch..."
git checkout main
git pull origin main
if git show-ref --quiet refs/heads/"$BRANCH_NAME"; then
  echo "🔁 Branch $BRANCH_NAME already exists. Resetting to main."
  git checkout "$BRANCH_NAME"
  git reset --hard origin/main
else
  git checkout -b "$BRANCH_NAME"
  echo "🌱 Created new branch: $BRANCH_NAME"
fi

# Step 3: Apply the patch
git apply "$PATCH_FILE"

# Step 4: Commit changes
git add .
git commit -m "$SUMMARY [task: $TASK_ID]"

# Step 5: Push branch
git push -u origin "$BRANCH_NAME"

# Step 6: Restore previous stash
if [ "$STASHED" -eq 1 ]; then
  echo "📦 Restoring stashed changes..."
  git stash pop
fi

# Step 7: Create PR
if command -v gh &> /dev/null; then
  gh pr create --title "$SUMMARY [task: $TASK_ID]" --body "Auto-generated patch from $PATCH_FILE" --base main --head "$BRANCH_NAME"
else
  echo "ℹ️ 'gh' CLI not found. Please create PR manually from branch: $BRANCH_NAME"
fi
