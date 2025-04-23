#!/bin/bash
set -e

echo "🧠 Starting AI-native patch promotion to feature branch..."

# Always work from repo root
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

# Step 1: Get patch file (prefer triggered one if available)
if [ -n "$TRIGGERED_PATCH" ]; then
  PATCH_FILE="$ROOT_DIR/.patches/$TRIGGERED_PATCH"
  echo "📎 Using triggered patch file: $PATCH_FILE"
else
  PATCH_FILE=$(ls -t "$ROOT_DIR/.patches"/*.diff | head -n 1)
  echo "📄 Found patch: $PATCH_FILE"
fi

if [ ! -f "$PATCH_FILE" ]; then
  echo "❌ ERROR: Patch file not found at $PATCH_FILE"
  exit 1
fi

PATCH_NAME=$(basename "$PATCH_FILE" .diff)
BRANCH_NAME="chatgpt/auto/${PATCH_NAME}"

echo "🌿 Creating branch: $BRANCH_NAME"

# Step 2: Auto-stash local changes to prevent checkout issues
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "🔒 Stashing local changes before switching branches..."
  git stash push -m "autostash-before-patch-apply"
fi

# Step 3: Ensure clean state and checkout main
if git show-ref --quiet refs/remotes/origin/main; then
  echo "📥 Fetching and checking out origin/main"
  git fetch origin
  git checkout -B main origin/main
else
  echo "❌ ERROR: origin/main not found"
  exit 1
fi

# Step 4: Handle remote or local branch reuse
git fetch origin "$BRANCH_NAME" || true

if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  echo "🔁 Local branch $BRANCH_NAME exists, checking it out..."
  git checkout "$BRANCH_NAME"
elif git ls-remote --exit-code --heads origin "$BRANCH_NAME" > /dev/null; then
  echo "🌐 Remote branch $BRANCH_NAME exists, creating local tracking branch..."
  git checkout -b "$BRANCH_NAME" --track origin/"$BRANCH_NAME"
else
  echo "🌱 Creating new local branch $BRANCH_NAME"
  git checkout -b "$BRANCH_NAME"
fi

# Debug check
echo "🧾 Checking existence of $PATCH_FILE"
ls -l "$PATCH_FILE" || echo "🚫 Still not found..."
echo "📂 Current directory: $(pwd)"
echo "📁 Contents of .patches:"
ls -la .patches || echo "🚫 .patches folder not found"

# Step 5: Apply the patch
cat "$PATCH_FILE" | patch -p1 || {
  echo "❌ Patch failed to apply. Cleaning up."
  exit 1
}

# Step 6: Stage supporting logs if present
[ -f docs/changelog.md ] && git add docs/changelog.md
[ -f logs/thought_trace.md ] && git add logs/thought_trace.md

# Step 7: Commit and push
git add .
git commit -m "[AutoPatch] Apply ${PATCH_NAME} from .patches/"
git push origin "$BRANCH_NAME"

# Step 8: Optionally open PR (if gh CLI is installed and configured)
if command -v gh &> /dev/null; then
  echo "📬 Opening pull request via GitHub CLI..."
  gh pr create --title "📦 Patch: ${PATCH_NAME}" \
               --body "Auto-generated patch from .patches by pod delivery loop." \
               --base main \
               --head "$BRANCH_NAME"
else
  echo "ℹ️ GitHub CLI not found. PR not created automatically."
fi

# Optional: Pop stash back (only in local dev, not CI)
if [ -z "$CI" ]; then
  if git stash list | grep -q "autostash-before-patch-apply"; then
    echo "🔓 Restoring stashed changes..."
    git stash pop || echo "⚠️ Merge conflict on stash pop. Run 'git status' and resolve manually."
  fi
else
  echo "💡 Skipping stash pop in CI (safe mode)"
fi

# Optional: Clean up the patch so it doesn’t get reapplied
rm -f "$PATCH_FILE"
echo "🧹 Cleaned up patch file: $PATCH_FILE"

echo "✅ Patch promoted to branch and ready for PR review!"
echo "🚀 Done!"