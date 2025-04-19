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

# Step 2: Auto-stash local changes to prevent checkout issues
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "🔒 Stashing local changes before switching branches..."
  git stash push -m "autostash-before-patch-apply"
fi

# Step 3: Ensure clean state and checkout main
git fetch origin

if git rev-parse --verify main >/dev/null 2>&1; then
  git checkout main
  git pull origin main
else
  echo "❌ ERROR: main branch not found"
  exit 1
fi

# Step 4: Handle remote or local branch reuse
git fetch origin "$BRANCH_NAME" || true

# Check if branch exists locally
if git show-ref --verify --quiet "refs/heads/$BRANCH_NAME"; then
  echo "🔁 Local branch $BRANCH_NAME exists, checking it out..."
  git checkout "$BRANCH_NAME"

# Check if it exists on the remote
elif git ls-remote --exit-code --heads origin "$BRANCH_NAME" > /dev/null; then
  echo "🌐 Remote branch $BRANCH_NAME exists, creating local tracking branch..."
  git checkout -b "$BRANCH_NAME" --track origin/"$BRANCH_NAME"

# Otherwise, create a fresh branch
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
cat "$PATCH_FILE" | patch -p1

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

# Optional: Pop stash back (for local dev, not CI)
if git stash list | grep -q "autostash-before-patch-apply"; then
  echo "🔓 Restoring stashed changes..."
  git stash pop
fi

echo "✅ Patch promoted to branch and ready for PR review!"
