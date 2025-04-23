#!/bin/bash
set -e

echo "📦 Promoting patch from ChatGPT repo to local Git repo..."

# Step 1: Define paths
SANDBOX_PATCHES="./chatgpt_repo/.patches"
LOCAL_PATCHES=".patches"

# Step 2: Get latest patch file from sandbox
PATCH_FILE=$(ls -t "$SANDBOX_PATCHES"/*.diff | head -n 1)

if [ ! -f "$PATCH_FILE" ]; then
  echo "❌ ERROR: No patch file found in $SANDBOX_PATCHES"
  exit 1
fi

PATCH_NAME=$(basename "$PATCH_FILE")
echo "📎 Found patch: $PATCH_NAME"

# Step 3: Copy to local repo
cp "$PATCH_FILE" "$LOCAL_PATCHES/$PATCH_NAME"
echo "✅ Copied to $LOCAL_PATCHES/$PATCH_NAME"

# Step 4: Promote to remote feature branch + PR
TRIGGERED_PATCH="$PATCH_NAME" bash scripts/create_pr_from_patch.sh
