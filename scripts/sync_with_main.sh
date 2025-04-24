#!/bin/bash
set -e

echo "📦 Syncing with remote 'main' branch..."

# Fetch latest changes from origin
git fetch origin

# Rebase local changes onto the latest remote main
echo "🔄 Rebasing local changes onto origin/main..."
git rebase origin/main

# Push updated local main to origin
echo "🚀 Pushing changes to origin/main..."
git push origin main

echo "✅ Push complete. Local and remote 'main' are now in sync!"
