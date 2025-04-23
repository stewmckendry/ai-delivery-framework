#!/bin/bash
set -e

echo "🧠 Fixing accidental commit to wrong branch..."

# Capture current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" = "main" ]; then
  echo "⚠️ You're already on main. Nothing to fix."
  exit 0
fi

# Get last commit hash
COMMIT_HASH=$(git rev-parse HEAD)
echo "🔍 Last commit: $COMMIT_HASH on branch $CURRENT_BRANCH"

# Checkout main
echo "🌿 Switching to main..."
git checkout main

# Cherry-pick the commit
echo "🍒 Cherry-picking commit to main..."
git cherry-pick $COMMIT_HASH

# Ask if user wants to push
read -p "✅ Cherry-picked to main. Push now? (y/n) " PUSH_MAIN
if [ "$PUSH_MAIN" = "y" ]; then
  git push origin main
fi

# Ask if user wants to clean GPT branch
read -p "🧼 Reset $CURRENT_BRANCH to match origin/main? (y/n) " RESET_GPT
if [ "$RESET_GPT" = "y" ]; then
  git checkout "$CURRENT_BRANCH"
  git reset --hard origin/main
  echo "✅ Reset $CURRENT_BRANCH to origin/main"
else
  echo "⚠️ $CURRENT_BRANCH still contains the commit."
fi

echo "🎯 Done!"
