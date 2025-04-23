#!/bin/bash
set -e

# Load patch file
PATCH_FILE="${TRIGGERED_PATCH:-$(ls -t .patches/*.diff | head -n 1)}"
PATCH_NAME=$(basename "$PATCH_FILE")
PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
PATCH_JSON="${LOG_DIR}/${PATCH_NAME%.diff}.json"
FULL_PATCH_PATH="$PATCH_FILE"

# If it's not a full path, prefix it with PATCH_DIR
if [ ! -f "$FULL_PATCH_PATH" ] && [ -f "$PATCH_DIR/$PATCH_FILE" ]; then
  FULL_PATCH_PATH="$PATCH_DIR/$PATCH_FILE"
fi

if [ ! -f "$FULL_PATCH_PATH" ]; then
  echo "❌ ERROR: Patch file not found: $FULL_PATCH_PATH"
  exit 1
fi

echo "📎 Using triggered patch file: $FULL_PATCH_PATH"

# Validate metadata file
if [ ! -f "$PATCH_JSON" ]; then
  echo "❌ Metadata not found: $PATCH_JSON"
  echo "🔍 Available metadata files:"
  ls "$LOG_DIR"/*.json 2>/dev/null || echo "⚠️ None found."
  exit 1
fi

# Step 0: Stash any current work to avoid overwriting
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Stashing uncommitted changes..."
  git stash push --keep-index -m "pre-patch-stash-$(date +%s)"
  STASHED=1
else
  STASHED=0
fi
echo "✅ Stashed changes."

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
echo "🧪 Checking patch before applying..."
git apply --check "$FULL_PATCH_PATH" || { echo "❌ Patch failed dry run."; exit 1; }
git apply "$FULL_PATCH_PATH"
echo "✅ Patch applied successfully."

# Step 4: Commit changes
echo "📝 Committing changes..."
git add .
git commit -m "$SUMMARY [task: $TASK_ID]"
echo "✅ Changes committed successfully."

# Step 5: Push branch
echo "🚀 Pushing branch to remote..."
git push -u origin "$BRANCH_NAME"
echo "✅ Branch pushed successfully."

# Step 6: Restore previous stash
if [ "$STASHED" -eq 1 ]; then
  echo "📦 Restoring stashed changes..."
  if git stash pop; then
    echo "✅ Stashed changes restored successfully."
  else
    echo "⚠️ Could not pop stash automatically. You may need to resolve conflicts manually."
  fi
fi

# Step 7: Create PR
if command -v gh &> /dev/null; then
  echo "📬 Creating PR..."
  gh pr create --title "$SUMMARY [task: $TASK_ID]" --body "Auto-generated patch from $PATCH_FILE" --base main --head "$BRANCH_NAME"
  echo "✅ PR created successfully."
else
  echo "ℹ️ 'gh' CLI not found. Please create PR manually from branch: $BRANCH_NAME"
fi
