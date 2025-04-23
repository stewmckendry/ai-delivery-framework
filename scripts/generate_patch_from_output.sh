#!/bin/bash
set -e

echo "🔄 Script initiated."

USE_TASK_YAML=0

echo "🔄 Parsing arguments."
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --task_id) TASK_ID="$2"; shift 2;;
        --summary) SUMMARY="$2"; shift 2;;
        --use_task_yaml) USE_TASK_YAML=1; shift;;
        *) echo "❌ Unknown option: $1"; exit 1;;
    esac
done
echo "✅ Arguments parsed."

if [ $USE_TASK_YAML -eq 1 ]; then
    echo "🔄 Using task.yaml to determine task details."
    TASK_YAML=".task/task.yaml"
    TASK_ID=$(yq '.tasks | to_entries[] | select(.value.ready == true and .value.done == false) | .key' "$TASK_YAML" | head -n 1 | tr -d '"')
    SUMMARY=$(yq ".tasks.$TASK_ID.description" "$TASK_YAML")
    OUTPUT_FILES=($(yq ".tasks.$TASK_ID.outputs[]" "$TASK_YAML" | tr -d '"'))
    echo "✅ Task details loaded from task.yaml."
else
    if [ -z "$TASK_ID" ] || [ -z "$SUMMARY" ]; then
        echo "❌ Usage: $0 --task_id TASK_ID --summary SUMMARY or --use_task_yaml"
        exit 1
    fi
    echo "🔄 Loading task details from provided arguments."
    OUTPUT_FILES=($(yq ".tasks.$TASK_ID.outputs[]" .task/task.yaml | tr -d '"'))
    echo "✅ Task details loaded from arguments."
fi

PATCH_DIR=".patches"
LOG_DIR=".logs/patches"
echo "🔄 Creating directories: $PATCH_DIR and $LOG_DIR."
mkdir -p "$PATCH_DIR" "$LOG_DIR"
echo "✅ Directories created."

OUTPUT_FOLDERS=()

for OUTPUT_FILE in "${OUTPUT_FILES[@]}"; do
    echo "🔄 Preparing output file: $OUTPUT_FILE."
    SOURCE_FILE="chatgpt_repo/outputs/$OUTPUT_FILE"
    DEST_FILE="$OUTPUT_FILE"
    mkdir -p "$(dirname $DEST_FILE)"
    cp "$SOURCE_FILE" "$DEST_FILE"
    git add --intent-to-add "$DEST_FILE"
    OUTPUT_FOLDERS+=("$(dirname $DEST_FILE)")
    echo "✅ Prepared: $DEST_FILE"
done

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PATCH_NAME="patch_${TIMESTAMP}_${TASK_ID}.diff"
PATCH_FILE="$PATCH_DIR/$PATCH_NAME"

echo "🔄 Creating patch file: $PATCH_FILE."
git diff --staged > "$PATCH_FILE"
echo "✅ Patch file created: $PATCH_FILE."

METADATA_FILE="$LOG_DIR/${PATCH_NAME%.diff}.json"
echo "🔄 Creating metadata file: $METADATA_FILE."
cat > "$METADATA_FILE" <<EOF
{
    "task_id": "$TASK_ID",
    "summary": "$SUMMARY",
    "output_folders": ["${OUTPUT_FOLDERS[@]}"]
}
EOF
echo "✅ Metadata file created: $METADATA_FILE."

echo "🔄 Triggering PR creation script."
bash scripts/create_pr_from_patch.sh --triggered "$PATCH_FILE"
echo "✅ PR creation script executed."

echo "🎉 Script completed successfully."