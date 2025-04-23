#!/bin/bash
set -e

echo "🚀 Starting patch promotion to remote branch..."

# Always work from repo root
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR"

PATCH_DIR=".patches"
LOG_DIR=".logs/patches"

# Step 1: Determine patch to promote
if [ -n "$TRIGGERED_PATCH" ]; then
  PATCH_FILE="$PATCH_DIR/$TRIGGERED_PATCH"
  echo "📎 Using triggered patch file: $PATCH_FILE"
else
  PATCH_FILE=$(ls -t "$PATCH_DIR"/*.diff | head -n 1)
  echo "📄 Found patch: $PATCH_FILE"
fi

# Sanity check
if [ ! -f "$PATCH_FILE" ]; then
  echo "❌ ERROR: Patch file not found at $PATCH_FILE"
  exit 1
fi

PATCH_NAME=$(basename "$PATCH_FILE" .diff)
PATCH_JSON="$LOG_DIR/${PATCH_NAME}.json"

# Sanity check for metadata
if [ ! -f "$PATCH_JSON" ]; then
  echo "❌ ERROR: Metadata not found at $PATCH_JSON"
  exit 1
fi

# Step 2: Extract metadata
TASK_ID=$(jq -r '.task_id' "$PATCH_JSON")
SUMMARY=$(jq -r '.summary' "$PATCH_JSON")
BRANCH_NAME="chatgpt/auto/${PATCH_NAME}"

# Step 3: Create branch, apply patch
git checkout -b "$BRANCH_NAME"
git apply "$PATCH_FILE"

# Step 4: Commit and push
git add .
git commit -m "Patch: ${TASK_ID} - ${SUMMARY}"
git push -u origin "$BRANCH_NAME"

# Step 5: Open PR if CLI available
if command -v gh &>/dev/null; then
  echo "🔗 Creating GitHub PR..."
  gh pr create \
    --title "Patch: ${TASK_ID}" \
    --body "${SUMMARY}" \
    --head "$BRANCH_NAME" \
    --base main
else
  echo "✅ Branch pushed: $BRANCH_NAME"
  echo "🔍 Please open a PR manually."
fi
