#!/bin/bash
set -e

# Step 1: Define the branch to get the last commit from
SOURCE_BRANCH="chatgpt/auto/patch_1.1_capture_project_goals_20250423_224614"

# Step 2: Checkout the main branch and ensure it's up-to-date
echo "🌿 Switching to main branch..."
git checkout main
git pull origin main

# Step 3: Cherry-pick the last commit from the source branch
echo "🍒 Cherry-picking the last commit from $SOURCE_BRANCH..."
LAST_COMMIT_HASH=$(git rev-parse "$SOURCE_BRANCH")
git cherry-pick "$LAST_COMMIT_HASH"

# Step 4: Push the changes to the main branch
echo "🚀 Pushing changes to main..."
git push origin main

echo "✅ Last commit from $SOURCE_BRANCH has been pushed to main."