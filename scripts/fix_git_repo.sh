#!/bin/bash
set -e

echo "🧹 Starting safe repo reset..."

# Show current git status
echo "🔍 Checking current git status..."
git status

# Step 1: Stash any uncommitted changes
if [ -n "$(git status --porcelain)" ]; then
  echo "📦 Stashing uncommitted changes..."
  git stash push --include-untracked -m "safe-repo-reset-$(date +%s)"
else
  echo "✅ No uncommitted changes to stash."
fi

# Step 2: Reset to remote main
echo "🔄 Resetting local main to match origin/main..."
git checkout main
git fetch origin
git reset --hard origin/main

# Step 3: Remove untracked files and directories (dry run first)
echo "🧪 DRY RUN: Untracked files/folders that would be removed:"
git clean -nd

echo ""
read -p "❓ Proceed to delete the above untracked files? (y/n): " CONFIRM
if [ "$CONFIRM" = "y" ]; then
  git clean -fd
  echo "✅ Untracked files removed."
else
  echo "❌ Aborted. Untracked files NOT removed."
fi

echo "✅ Repo reset complete. You can now re-run your patch workflow."
