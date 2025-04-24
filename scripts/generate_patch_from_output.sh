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
echo "🔄 Searching for latest ZIP in outputs folder..."
ZIP_FILE=$(ls -t chatgpt_repo/outputs/*.zip | head -n 1)

if [ ! -f "$ZIP_FILE" ]; then
  echo "❌ No finalized output ZIP file found in chatgpt_repo/outputs/"
  exit 1
fi

echo "✅ Found ZIP file: $ZIP_FILE"
echo "🔄 Unzipping file..."
TMP_DIR=$(mktemp -d)
unzip "$ZIP_FILE" -d "$TMP_DIR"


echo "🔄 Searching for metadata.json in unzipped folder..."
METADATA_FILE="$TMP_DIR/metadata.json"
if [ ! -f "$METADATA_FILE" ]; then
  echo "❌ metadata.json not found inside ZIP"
  exit 1
fi
echo "✅ Metadata file found: $METADATA_FILE"

echo "🔄 Loading metadata..."
TASK_ID=$(jq -r '.task_id' "$METADATA_FILE")
SUMMARY=$(jq -r '.summary' "$METADATA_FILE")
echo "✅ Metadata loaded:"
echo "   - Task ID: $TASK_ID"
echo "   - Summary: $SUMMARY"

echo "🔄 Reading output file paths from metadata"
OUTPUT_FILES=($(jq -r '.output_files[]' "$METADATA_FILE"))
echo "✅ Output files found: ${#OUTPUT_FILES[@]}"
for FILE in "${OUTPUT_FILES[@]}"; do
  cp "$TMP_DIR/$FILE" "$FILE"
  mkdir -p "$(dirname "$FILE")"
  git add "$FILE"
  echo "✅ Staged: $FILE"
done
echo "🔄 Total output files staged: ${#OUTPUT_FILES[@]}"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PATCH_NAME="patch_${TASK_ID}_${TIMESTAMP}.diff"
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


