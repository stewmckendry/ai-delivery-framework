#!/bin/bash
set -e

echo "🧐 Starting AI-native patch promotion to feature branch..."

# Step 1: Find the .diff file
PATCH_FILE=$(find .patches -name '*.diff' | head -n 1)
if [ -z "$PATCH_FILE" ]; then
  echo "❌ No .diff file found in .patches/"
  exit 1
fi

PATCH_NAME=$(basename "$PATCH_FILE" .diff)
BRANCH_NAME="chatgpt/auto/${PATCH_NAME}"

echo "📄 Found patch: $PATCH_FILE"
echo "🌿 Creating branch: $BRANCH_NAME"

# Step 2: Ensure clean state and checkout main
git stash --include-untracked
git fetch origin
git checkout main
git pull origin main

# Step 3: Create and switch to new feature branch
git checkout -b "$BRANCH_NAME"

# Step 4: Apply the patch
patch -p1 < "$PATCH_FILE"

# Step 5: Stage supporting logs if present
[ -f docs/changelog.md ] && git add docs/changelog.md
[ -f logs/thought_trace.md ] && git add logs/thought_trace.md

# Step 6: Commit and push
git add .
git commit -m "[AutoPatch] Apply ${PATCH_NAME} from .patches/"
git push origin "$BRANCH_NAME"

# Step 7: Optionally open PR (if gh CLI is installed and configured)
if command -v gh &> /dev/null; then
  echo "📬 Opening pull request via GitHub CLI..."
  gh pr create --title "📦 Patch: ${PATCH_NAME}" \
               --body "Auto-generated patch from .patches by pod delivery loop." \
               --base main \
               --head "$BRANCH_NAME"
else
  echo "ℹ️ GitHub CLI not found. PR not created automatically."
fi

echo "✅ Patch promoted to branch and ready for PR review!"
