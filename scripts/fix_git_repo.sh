#!/bin/bash
set -e

echo "🛠️ Cleaning Git repo workspace safely..."

# Step 1: Show current status
echo "🔍 Git Status:"
git status

# Step 2: Unstage all changes (keep local modifications)
echo "🔄 Unstaging any staged changes..."
git reset

# Step 3: Show unstaged diff preview
echo "🔍 Preview of unstaged local changes:"
git diff || echo "(no unstaged changes)"

# Step 4: Ask user before hard reset
echo ""
read -p "⚠️ Do you want to fully reset your repo and remove all local changes and untracked files? [y/N] " confirm

if [[ "$confirm" =~ ^[Yy]$ ]]; then
  echo "⚠️ Resetting and cleaning repo..."
  git reset --hard HEAD
  git clean -fd
  echo "✅ Repo has been reset to latest committed state."
else
  echo "❌ Cancelled. Repo was not reset."
fi

# Final status
echo "✅ Done. Final status:"
git status