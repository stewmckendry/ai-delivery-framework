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
ZIP_FILE=$(find chatgpt_repo/outputs -name "*.zip" -type f | sort -r | head -n 1)

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

echo "Checking for task.yaml to extract category for branch name..."
TASKS_FILE="task.yaml"
if [ ! -f "$TASKS_FILE" ]; then
  echo "❌ task.yaml not found. Cannot determine category."
  exit 1
fi

echo "🧪 Debug: Checking task key in task.yaml"
yq e ".tasks | keys" "$TASKS_FILE"

echo "Searching for task category for branch name in task.yaml..."
CATEGORY=$(yq e ".tasks.\"$TASK_ID\".category" "$TASKS_FILE")
if [ -z "$CATEGORY" ] || [[ "$CATEGORY" == "null" ]]; then
  echo "❌ No category defined for task $TASK_ID in task.yaml"
  exit 1
fi

echo "✅ Task category from task.yaml: $CATEGORY"
BRANCH_NAME="chatgpt/auto/$CATEGORY/$TASK_ID"
echo "🔄 Setting branch name: $BRANCH_NAME"

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
echo "🔍 Git status:"
git status --short

echo "🔍 Staged diff:"
GIT_PAGER=cat git diff --cached

git diff --staged > "$PATCH_FILE"

if [ ! -s "$PATCH_FILE" ]; then
  echo "❌ Patch file is empty or failed to generate"
  echo "🔍 Tip: Check that the file has actually changed."
  git status
  exit 1
fi


echo "✅ Patch file created: $PATCH_FILE"

METADATA_OUT="$LOG_DIR/${PATCH_NAME%.diff}.json"
echo "🔄 Copying metadata file to patch logs"
cp "$METADATA_FILE" "$METADATA_OUT"
echo "✅ Metadata file saved: $METADATA_OUT"

echo "🔄 Saving branch name to metadata file..."
jq --arg branch "$BRANCH_NAME" '. + {branch_name: $branch}' "$METADATA_FILE" > "$METADATA_OUT"
echo "✅ Metadata file updated with branch name: $BRANCH_NAME"

echo "🔄 Checking for reasoning trace..."
REASONING_TRACE_FILE="$TMP_DIR/reasoning_trace.md"
if [ -f "$REASONING_TRACE_FILE" ]; then
  echo "✅ Reasoning trace found: $REASONING_TRACE_FILE"
else
  echo "ℹ️ No reasoning trace file found."
  REASONING_TRACE_FILE=""
fi

echo "🔄 Marking task as complete and generating changelog..."
bash scripts/complete_task.sh "$TASK_ID" "$REASONING_TRACE_FILE"
echo "✅ Task completion logged."

echo "🔄 Checking for prompt_used.txt..."
PROMPT_FILE="$TMP_DIR/prompt_used.txt"
PROMPT_LOG_DIR="prompts/used"

echo "🔍 Extracting pod_owner from task.yaml to use in prompt file path (prompt files organized by pod)..."
pod_owner=$(yq e ".tasks.\"$TASK_ID\".pod_owner" "$TASKS_FILE")
if [ -z "$pod_owner" ] || [[ "$pod_owner" == "null" ]]; then
  echo "❌ No pod_owner defined for task $TASK_ID in task.yaml"
  exit 1
fi
echo "✅ Assigned Pod: $pod_owner"
PROMPT_LOG_PATH="${PROMPT_LOG_DIR}/${pod_owner}/${TASK_ID}_prompt.txt"

if [ -f "$PROMPT_FILE" ]; then
  mkdir -p "$(dirname "$PROMPT_LOG_PATH")"
  cp "$PROMPT_FILE" "$PROMPT_LOG_PATH"
  echo "✅ Prompt used saved to: $PROMPT_LOG_PATH"
else
  echo "ℹ️ No prompt_used.txt file found in ZIP."
fi

# Handle memory.yaml if exists
MEMORY_FILE="$TMP_DIR/memory.yaml"
if [ -f "$MEMORY_FILE" ]; then
  echo "✅ Found memory.yaml inside ZIP. Staging for Git."
  cp "$MEMORY_FILE" "memory.yaml"
  git add "memory.yaml"
else
  echo "ℹ️ No memory.yaml found in ZIP."
fi

# Handle handoff notes if they exist
HANDOFF_DIR="$TMP_DIR/handoff_notes"
if [ -d "$HANDOFF_DIR" ]; then
  echo "✅ Found handoff_notes folder. Staging handoff notes."
  mkdir -p ".logs/handoff"
  cp "$HANDOFF_DIR"/*.md ".logs/handoff/"
  for file in "$HANDOFF_DIR"/*.md; do
    [ -e "$file" ] && git add ".logs/handoff/$(basename "$file")"
    echo "✅ Staged handoff note: $(basename "$file")"
  done
else
  echo "ℹ️ No handoff notes found in ZIP."
fi


echo "🔄 Triggering PR creation script"
bash scripts/create_pr_from_patch.sh --triggered "$PATCH_FILE"
echo "✅ PR creation script executed"

echo "🎉 Script completed successfully."