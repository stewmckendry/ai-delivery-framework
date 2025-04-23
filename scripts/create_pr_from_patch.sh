#!/bin/bash
set -e

echo "🚀 Initiating script: create_pr_from_patch.sh"

# Parse args
echo "🔍 Parsing arguments..."
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --triggered) TRIGGERED_PATCH="$2"; shift 2;;
    *) echo "❌ Unknown option: $1"; exit 1;;
  esac
done
echo "✅ Arguments parsed successfully."

# Load patch file
echo "🔍 Loading patch file..."
PATCH_FILE="${TRIGGERED_PATCH:-$(ls -t .patches/*.diff | head -n 1)}"
PATCH_NAME=$(basename "$PATCH_FILE")
PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
PATCH_JSON="${LOG_DIR}/${PATCH_NAME%.diff}.json"
FULL_PATCH_PATH="$PATCH_FILE"

# If it's not a full path, prefix it
if [ ! -f "$FULL_PATCH_PATH" ] && [ -f "$PATCH_DIR/$PATCH_FILE" ]; then
  FULL_PATCH_PATH="$PATCH_DIR/$PATCH_FILE"
fi

if [ ! -f "$FULL_PATCH_PATH" ]; then
  echo "❌ ERROR: Patch file not found: $FULL_PATCH_PATH"
  exit 1
fi
echo "📎 Using triggered patch file: $FULL_PATCH_PATH"

# Validate metadata file
echo "🔍 Validating metadata file..."
if [ ! -f "$PATCH_JSON" ]; then
  echo "❌ Metadata not found: $PATCH_JSON"
  echo "🔍 Available metadata files:"
  ls "$LOG_DIR"/*.json 2>/dev/null || echo "⚠️ None found."
  exit 1
fi
echo "✅ Metadata file validated successfully."

# Step 0: Stash current work
echo "📦 Checking for uncommitted changes to stash..."
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Stashing uncommitted changes..."
  git stash push --keep-index -m "pre-patch-stash-$(date +%s)"
  STASHED=1
else
  STASHED=0
fi
echo "✅ Stashed changes."

# Step 1: Extract metadata
echo "🔍 Extracting metadata from JSON..."
TASK_ID=$(jq -r .task_id "$PATCH_JSON")
SUMMARY=$(jq -r .summary "$PATCH_JSON")
BRANCH_NAME="chatgpt/auto/${PATCH_NAME%.diff}"
echo "✅ Metadata extracted successfully."

# Step 2: Update main and switch to patch branch
echo "🔄 Updating main branch and switching to patch branch..."
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
echo "✅ Branch setup completed."

# Step 3: Pre-clean files declared in patch
echo "🧹 Cleaning up conflicting files..."
grep '^+++ b/' "$FULL_PATCH_PATH" | awk '{print $2}' | while read -r file; do
  if [ -f "$file" ]; then
  echo "❌ Removing pre-existing file: $file"
  rm "$file"
  fi
done
echo "✅ Conflicting files cleaned up."

# Step 4: Apply the patch
echo "🧪 Performing dry run for patch application..."
if ! git apply --check "$FULL_PATCH_PATH"; then
  echo "❌ Patch failed dry run."
  exit 1
fi
echo "✅ Dry run successful. Applying patch..."
git apply "$FULL_PATCH_PATH"
echo "✅ Patch applied successfully."

# Step 5: Commit changes
echo "📝 Committing changes..."
git add .
git commit -m "$SUMMARY [task: $TASK_ID]"
echo "✅ Changes committed successfully."

# Step 6: Push branch
echo "🚀 Pushing branch to remote..."
git push -u origin "$BRANCH_NAME"
echo "✅ Branch pushed successfully."

# Step 7: Restore stash
if [ "$STASHED" -eq 1 ]; then
  echo "📦 Restoring stashed changes..."
  if git stash pop; then
  echo "✅ Stashed changes restored successfully."
  else
  echo "⚠️ Could not pop stash automatically."
  fi
fi

# Step 8: Create PR
echo "📬 Creating pull request..."
if command -v gh &> /dev/null; then
  gh pr create --title "$SUMMARY [task: $TASK_ID]" --body "Auto-generated patch from $PATCH_FILE" --base main --head "$BRANCH_NAME"
  echo "✅ Pull request created successfully."
else
  echo "ℹ️ 'gh' CLI not found. Please create PR manually from branch: $BRANCH_NAME"
fi

echo "🎉 Script completed successfully!"

