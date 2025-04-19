#!/bin/bash
set -e

echo "🧠 Starting AI-native patch promotion to feature branch..."

# Always work from repo root
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# Step 1: Find the .diff file
PATCH_FILE=$(find "$ROOT_DIR/.patches" -name '*.diff' | head -n 1)

if [ ! -f "$PATCH_FILE" ]; then
  echo "❌ ERROR: Patch file not found at $PATCH_FILE"
  exit 1
fi

PATCH_NAME=$(basename "$PATCH_FILE" .diff)
BRANCH_NAME="chatgpt/auto/${PATCH_NAME}"

echo "📄 Found patch: $PATCH_FILE"
echo "🌿 Creating branch: $BRANCH_NAME"

# Step 2: Ensure clean state and checkout main
# Commenting out stash for now — it's likely wiping the .diff
# git stash --include-untracked

git fetch origin
git checkout main
git pull origin main

# Step 3: Create and switch to new feature branch
git checkout -b "$BRANCH_NAME"

# Debug check
echo "🧾 Checking existence of $PATCH_FILE"
ls -l "$PATCH_FILE" || echo "🚫 Still not found..."
echo "📂 Current directory: $(pwd)"
echo "📁 Contents of .patches:"
ls -la .patches || echo "🚫 .patches folder not found"

# Step 4: Apply the patch
cat "$PATCH_FILE" | patch -p1

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
