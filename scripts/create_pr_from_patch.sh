#!/bin/bash
set -e

echo "🚀 Initiating script..."

# Parse args
echo "🔍 Parsing arguments..."
while [[ "$#" -gt 0 ]]; do
  case $1 in
    --triggered) TRIGGERED_PATCH="$2"; shift 2;;
    *) echo "❌ Unknown option: $1"; exit 1;;
  esac
done
echo "✅ Arguments parsed successfully."

PATCH_FILE="${TRIGGERED_PATCH:-$(ls -t .patches/*.diff | head -n 1)}"
PATCH_NAME=$(basename "$PATCH_FILE")
PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
PATCH_JSON="${LOG_DIR}/${PATCH_NAME%.diff}.json"
FULL_PATCH_PATH="$PATCH_FILE"

echo "🔍 Resolving patch file..."
if [ ! -f "$FULL_PATCH_PATH" ] && [ -f "$PATCH_DIR/$PATCH_FILE" ]; then
  FULL_PATCH_PATH="$PATCH_DIR/$PATCH_FILE"
fi

if [ ! -f "$FULL_PATCH_PATH" ]; then
  echo "❌ ERROR: Patch file not found: $FULL_PATCH_PATH"
  exit 1
fi
echo "✅ Patch file resolved: $FULL_PATCH_PATH"

echo "🔍 Checking metadata file..."
if [ ! -f "$PATCH_JSON" ]; then
  echo "❌ Metadata not found: $PATCH_JSON"
  echo "🔍 Available metadata files:"
  ls "$LOG_DIR"/*.json 2>/dev/null || echo "⚠️ None found."
  exit 1
fi
echo "✅ Metadata file found: $PATCH_JSON"

echo "🔍 Checking for uncommitted changes..."
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Stashing uncommitted changes..."
  git stash push --keep-index -m "pre-patch-stash-$(date +%s)"
  STASHED=1
  echo "✅ Changes stashed successfully."
else
  STASHED=0
  echo "✅ No uncommitted changes found."
fi

TASK_ID=$(jq -r .task_id "$PATCH_JSON")
SUMMARY=$(jq -r .summary "$PATCH_JSON")
BRANCH_NAME="chatgpt/auto/${PATCH_NAME%.diff}"

echo "🔄 Updating main branch..."
git checkout main
git pull origin main
echo "✅ Main branch updated successfully."

echo "🔍 Checking if branch $BRANCH_NAME exists..."
if git show-ref --quiet refs/heads/"$BRANCH_NAME"; then
  echo "🔁 Branch $BRANCH_NAME already exists. Resetting to main."
  git checkout "$BRANCH_NAME"
  git reset --hard origin/main
  echo "✅ Branch reset to main."
else
  git checkout -b "$BRANCH_NAME"
  echo "🌱 Created new branch: $BRANCH_NAME"
fi

echo "🧹 Cleaning up conflicting files..."
grep '^+++ b/' "$FULL_PATCH_PATH" | awk '{print $2}' | while read -r file; do
  if [ -f "$file" ]; then
  echo "❌ Removing pre-existing file: $file"
  git reset HEAD "$file" 2>/dev/null || true
  git checkout HEAD -- "$file" 2>/dev/null || true
  git rm --cached "$file" 2>/dev/null || true
  rm "$file" 2>/dev/null || true
  fi
done
echo "✅ Conflicting files cleaned up."

echo "🧪 Performing dry run of patch application..."
if git apply --check "$FULL_PATCH_PATH"; then
  echo "✅ Dry run successful. Applying patch..."
  git apply "$FULL_PATCH_PATH"
  echo "✅ Patch applied successfully."
else
  echo "❌ Patch failed dry run."
  exit 1
fi

echo "📝 Committing changes..."
git add .
git commit -m "$SUMMARY [task: $TASK_ID]"
echo "✅ Changes committed successfully."

echo "🚀 Pushing branch to remote..."
git push -u origin "$BRANCH_NAME"
echo "✅ Branch pushed successfully."

if [ "$STASHED" -eq 1 ]; then
  echo "📦 Restoring stashed changes..."
  if git stash pop; then
  echo "✅ Stashed changes restored successfully."
  else
  echo "⚠️ Could not pop stash automatically."
  fi
fi

if command -v gh &> /dev/null; then
  echo "📬 Creating PR..."
  if gh pr create --title "$SUMMARY [task: $TASK_ID]" --body "Auto-generated patch from $PATCH_FILE" --base main --head "$BRANCH_NAME"; then
  echo "✅ PR created successfully."
  else
  echo "❌ Failed to create PR."
  fi
else
  echo "ℹ️ 'gh' CLI not found. Please create PR manually from branch: $BRANCH_NAME"
fi

echo "🎉 Script completed successfully."
