#!/bin/bash
set -e

TASK_ID=$1
REASONING_FILE=$2

if [ -z "$TASK_ID" ]; then
  echo "❌ Usage: bash scripts/complete_task.sh <task_id> [optional_reasoning_file.md]"
  exit 1
fi

TASK_FILE="task.yaml"
PATCH_METADATA=$(ls .logs/patches/patch_${TASK_ID}_*.json | head -n 1)
if [ ! -f "$PATCH_METADATA" ]; then
  echo "❌ No patch metadata found for task $TASK_ID."
  exit 1
fi
CHANGELOG_FILE=".logs/changelogs/${TASK_ID}.md"
TRACE_FILE=".logs/reasoning/${TASK_ID}_trace.md"

echo "🔍 Updating task.yaml to mark $TASK_ID as complete..."

yq e -i ".tasks.\"$TASK_ID\".done = true" "$TASK_FILE"
yq e -i ".tasks.\"$TASK_ID\".status = \"complete\"" "$TASK_FILE"
echo "✅ task.yaml updated."

echo "📄 Generating changelog from patch summary..."
SUMMARY=$(jq -r '.summary' $(ls -t $PATCH_METADATA | head -n 1))
echo -e "# ✨ Changelog for $TASK_ID\n\n## Summary\n$SUMMARY" > "$CHANGELOG_FILE"
echo "✅ Changelog written to $CHANGELOG_FILE"

if [ -n "$REASONING_FILE" ] && [ -f "$REASONING_FILE" ]; then
  echo "🧠 Copying reasoning trace..."
  cp "$REASONING_FILE" "$TRACE_FILE"
  echo "✅ Reasoning trace saved to $TRACE_FILE"
else
  echo "ℹ️ No reasoning trace provided."
fi

echo "🎉 Task completion logged successfully."
