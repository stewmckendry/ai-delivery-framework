#!/bin/bash
set -e

echo "🔄 Script initiated."

PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
OUTPUTS_DIR="chatgpt_repo/outputs"
echo "🔄 Creating directories: $PATCH_DIR and $LOG_DIR."
mkdir -p "$PATCH_DIR" "$LOG_DIR"
echo "✅ Directories created."

echo "🔄 Loading metadata from latest file in $LOG_DIR"
METADATA_FILE=$(ls -t "$LOG_DIR"/*.json | head -n 1)

if [ ! -f "$METADATA_FILE" ]; then
  echo "❌ No metadata file found in $LOG_DIR"
  exit 1
fi

TASK_ID=$(jq -r '.task_id' "$METADATA_FILE")
SUMMARY=$(jq -r '.summary' "$METADATA_FILE")
OUTPUT_FOLDERS=($(jq -r '.output_folders[]' "$METADATA_FILE"))

echo "✅ Metadata loaded:"
echo "   - Task ID: $TASK_ID"
echo "   - Summary: $SUMMARY"
echo "   - Target Folders: ${OUTPUT_FOLDERS[*]}"

echo "🔄 Finding output files..."
OUTPUT_FILES=($(ls "$OUTPUTS_DIR"))

if [ ${#OUTPUT_FILES[@]} -eq 0 ]; then
  echo "❌ No output files found in $OUTPUTS_DIR"
  exit 1
fi

STAGED_FILES=()
for OUTPUT_FILE in "${OUTPUT_FILES[@]}"; do
  for FOLDER in "${OUTPUT_FOLDERS[@]}"; do
    DEST_PATH="$FOLDER/$OUTPUT_FILE"
    mkdir -p "$(dirname "$DEST_PATH")"
    cp "$OUTPUTS_DIR/$OUTPUT_FILE" "$DEST_PATH"
    git add "$DEST_PATH"
    STAGED_FILES+=("$DEST_PATH")
    echo "✅ Staged file: $DEST_PATH"
  done
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
echo "🔄 Writing metadata file: $METADATA_OUT"
cat > "$METADATA_OUT" <<EOF
{
  "task_id": "$TASK_ID",
  "summary": "$SUMMARY",
  "output_folders": ["${OUTPUT_FOLDERS[@]}"]
}
EOF
echo "✅ Metadata file written"

echo "🔄 Triggering PR creation script"
bash scripts/create_pr_from_patch.sh --triggered "$PATCH_FILE" --meta "$TEMP_JSON"
echo "✅ PR creation script executed"

echo "🎉 Script completed successfully."



