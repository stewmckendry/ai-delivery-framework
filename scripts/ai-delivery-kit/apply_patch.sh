#!/bin/bash

# 📌 apply_patch.sh
# Usage: ./scripts/apply_patch.sh gpt_patch_f4.3.diff
# Description: Applies a GPT-generated patch to a new feature branch and pushes it

set -e  # Stop on any error

# CONFIGURATION
REPO_URL="https://github.com/stewmckendry/ai-native-delivery.git"
REPO_NAME="ai-native-delivery"
BRANCH_NAME="chatgpt/dev/f4.3_rtp_guidance"
PATCH_FILE="$1"

if [ -z "$PATCH_FILE" ]; then
  echo "❌ Please provide a patch file."
  echo "Usage: ./scripts/apply_patch.sh gpt_patch_f4.3.diff"
  exit 1
fi

# ✅ Step 1: Clone the repo if not already cloned
if [ ! -d "$REPO_NAME/.git" ]; then
  echo "📦 Cloning repo..."
  git clone "$REPO_URL"
fi

cd "$REPO_NAME"

# ✅ Step 2: Create feature branch
if git rev-parse --verify "$BRANCH_NAME" >/dev/null 2>&1; then
  echo "ℹ️ Branch $BRANCH_NAME already exists, checking it out"
else
  echo "🌱 Creating new branch: $BRANCH_NAME"
  git checkout -b "$BRANCH_NAME"
fi

git checkout "$BRANCH_NAME"

# ✅ Step 3: Apply patch
echo "📄 Applying patch from $PATCH_FILE..."
patch -p1 < "../$PATCH_FILE"

# ✅ Step 4: Commit and push
echo "📤 Committing and pushing..."
git add .
git commit -m "[AutoPatch] Apply $PATCH_FILE to $BRANCH_NAME"
git push origin "$BRANCH_NAME"

echo "✅ Patch applied and pushed to $BRANCH_NAME"
