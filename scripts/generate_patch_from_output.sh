#!/bin/bash
set -e

echo "🔄 Script initiated."

PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
OUTPUTS_DIR="chatgpt_repo/outputs"
echo "🔄 Creating directories: $PATCH_DIR and $LOG_DIR."
mkdir -p "$PATCH_DIR" "$LOG_DIR"
echo "✅ Directories created."

echo "🔄 Loading metadata from outputs folder"
METADATA_FILE="chatgpt_repo/outputs/metadata.json"

if [ ! -f "$METADATA_FILE" ]; then
  echo "❌ No metadata file found in $LOG_DIR"
  exit 1
fi

TASK_ID=$(jq -r '.task_id' "$METADATA_FILE")
SUMMARY=$(jq -r '.summary' "$METADATA_FILE")
echo "✅ Metadata loaded:"
echo "   - Task ID: $TASK_ID"
echo "   - Summary: $SUMMARY"

echo "🔄 Looking for ZIP in $OUTPUTS_DIR"
ZIP_FILE=$(ls "$OUTPUTS_DIR"/*.zip | head -n 1)

if [ ! -f "$ZIP_FILE" ]; then
  echo "❌ No ZIP file found in $OUTPUTS_DIR"
  exit 1
fi

echo "✅ Found ZIP: $ZIP_FILE"
TMP_DIR=$(mktemp -d)
unzip "$ZIP_FILE" -d "$TMP_DIR"

echo "🔄 Reading output file paths from metadata"
OUTPUT_FILES=($(jq -r '.output_files[]' "$METADATA_FILE"))

for FILE in "${OUTPUT_FILES[@]}"; do
  cp "$TMP_DIR/$FILE" "$FILE"
  mkdir -p "$(dirname "$FILE")"
  git add "$FILE"
  echo "✅ Staged: $FILE"
done

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PATCH_NAME="patch_${TIMESTAMP}_${TASK_ID}.diff"
PATCH_FILE="$PATCH_DIR/$PATCH_NAME"

echo "🔄 Creating patch file: $PATCH_FILE"
git diff --staged > "$PATCH_FILE"

if [ ! -s "$PATCH_FILE" ]; then
  echo "❌ Patch file is empty or failed to generate"
  exit 1
fi

echo "✅ Patch file created: $PATCH_FILE"

METADATA_OUT="$LOG_DIR/${PATCH_NAME%.diff}.json"
echo "🔄 Copying metadata file to patch logs"
cp "$METADATA_FILE" "$METADATA_OUT"
echo "✅ Metadata file saved: $METADATA_OUT"

echo "🔄 Triggering PR creation script"
bash scripts/create_pr_from_patch.sh --triggered "$PATCH_FILE"
echo "✅ PR creation script executed"

echo "🎉 Script completed successfully."


