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

echo "🔍 Extracting metadata..."
TASK_ID=$(jq -r .task_id "$PATCH_JSON")
SUMMARY=$(jq -r .summary "$PATCH_JSON")
pod_owner=$(yq e ".tasks.\"$TASK_ID\".pod_owner" task.yaml)
echo "✅ Metadata loaded:"
echo "   - Task ID: $TASK_ID"
echo "   - Summary: $SUMMARY"
echo "   - Assigned Pod: $pod_owner"

echo "Extracting branch name..."
BRANCH_NAME=$(jq -r .branch_name "$PATCH_JSON")
if [ -z "$BRANCH_NAME" ] || [[ "$BRANCH_NAME" == "null" ]]; then
  echo "❌ branch_name not found in metadata. Please regenerate patch with updated script."
  exit 1
fi
echo "✅ Branch name extracted: $BRANCH_NAME"

echo "🔍 Setting file paths..."
CHANGELOG_FILE=".logs/changelogs/${TASK_ID}.md"
REASONING_FILE=".logs/reasoning/${TASK_ID}_trace.md"
PROMPT_FILE="prompts/used/${pod_owner}/${TASK_ID}_prompt.txt"
echo "✅ File paths set:"
echo "   - Changelog: $CHANGELOG_FILE"
echo "   - Reasoning: $REASONING_FILE"
echo "   - Prompt: $PROMPT_FILE"

echo "🔄 Updating main branch..."
git checkout main
git pull origin main
echo "✅ Main branch updated successfully."

echo "🔍 Checking if branch $BRANCH_NAME exists..."
if git show-ref --quiet refs/heads/"$BRANCH_NAME"; then
  echo "🔁 Branch $BRANCH_NAME already exists. Resetting to main."
  echo "📦 Stashing any working changes to avoid conflict..."
  git stash push -m "temp-stash-for-branch-reset"
  echo "📂 Switching to existing branch: $BRANCH_NAME"
  git checkout "$BRANCH_NAME" || {
    echo "❌ Failed to switch to branch. Aborting."; exit 1;
  }
  echo "♻️ Resetting branch to match origin/main"
  git reset --hard origin/main
  echo "✅ Branch reset to main."
else
  git checkout -b "$BRANCH_NAME"
  echo "🌱 Created new branch: $BRANCH_NAME"
fi

echo "🧹 Cleaning up conflicting files..."
grep '^+++ b/' "$FULL_PATCH_PATH" | awk '{sub("^b/", "", $2); print $2}' | while read -r file; do
  echo "🔍 Checking for conflict: $file"

  if [ -f "$file" ]; then
    echo "⚠️ File exists in working directory: $file"

    if git ls-files --error-unmatch "$file" > /dev/null 2>&1; then
      echo "🔎 Tracked by Git. Performing git cleanup:"
      git status --short "$file" || true
      git reset HEAD "$file" 2>/dev/null || true
      git checkout HEAD -- "$file" 2>/dev/null || true
      git rm --cached "$file" 2>/dev/null || true
    else
      echo "🆕 File is untracked. Will delete manually."
    fi

    echo "🗑 Deleting file from disk..."
    rm "$file" 2>/dev/null || echo "⚠️ Failed to delete $file"
    echo "♻️ Restoring $file from main branch"
    git checkout origin/main -- "$file"
  else
    echo "✅ No conflicting file for: $file"
  fi
done
echo "✅ Conflicting file check complete."


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

PR_BODY_FILE=$(mktemp)
{
  echo "## ✨ What was added?"
  echo "- Covers task: \`$TASK_ID\`"
  jq -r '.output_files[]' "$PATCH_JSON" | sed 's/^/- New file: `/' | sed 's/$/`/'
  echo
  echo "## 🎯 Why it matters"
  cat "$CHANGELOG_FILE" 2>/dev/null || echo "_No changelog found._"
  echo
  if [ -f "$REASONING_FILE" ]; then
    echo "## 🧠 Thought process"
    cat "$REASONING_FILE"
    echo
  fi
  echo "## 📄 Related"
  echo "- Task ID: $TASK_ID"
  if [ -f "$PROMPT_FILE" ]; then
    echo "## 📜 Prompt used"
    head -n 30 "$PROMPT_FILE"
    echo
  else
    echo "## 📜 Prompt used"
    echo "_Prompt text not found for task $TASK_ID._"
    echo
  fi

} > "$PR_BODY_FILE"

if command -v gh &> /dev/null; then
  echo "📬 Creating PR..."
  if gh pr create --title "$SUMMARY [task: $TASK_ID]" --body "$(cat "$PR_BODY_FILE")" --base main --head "$BRANCH_NAME"; then
    echo "✅ PR created successfully."
  else
    echo "❌ Failed to create PR."
  fi
  rm "$PR_BODY_FILE"
else
  echo "ℹ️ 'gh' CLI not found. Please create PR manually from branch: $BRANCH_NAME"
fi

echo "🎉 Script completed successfully."
