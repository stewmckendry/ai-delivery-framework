#!/bin/bash

# CONFIG — customize for your repo
GITHUB_USER="stewmckendry"
REPO_NAME="ai-delivery-framework"
BRANCH_NAME="main"

echo "🧠 Indexing repo files into memory_stub.yaml with auto-assigned pod_owner..."

# Go to repo root
ROOT_DIR=$(git rev-parse --show-toplevel)
cd "$ROOT_DIR" || exit 1

# Output file
OUTFILE="memory_stub.yaml"
> "$OUTFILE"

# Function to auto-assign pod_owner
assign_pod_owner() {
  local path="$1"

  if [[ "$path" == docs/* || "$path" == .github/* || "$path" == scripts/* || "$path" == README.md ]]; then
    echo "WoW Pod"
  else
    echo ""
  fi
}

# Find all files (skip archive/, .git/, etc.)
find . -type f \
  -not -path "*/.git/*" \
  -not -path "*/__pycache__/*" \
  -not -path "*/archive/*" \
  -not -path "*.DS_Store" \
  | while read -r filepath; do
    ext="${filepath##*.}"
    short_path="${filepath#./}"
    encoded_path=$(echo "$short_path" | sed 's| |%20|g')
    raw_url="https://raw.githubusercontent.com/${GITHUB_USER}/${REPO_NAME}/${BRANCH_NAME}/${encoded_path}"
    last_updated=$(git log -1 --format="%ad" --date=short "$filepath" 2>/dev/null)
    pod_owner=$(assign_pod_owner "$short_path")

    echo "- path: ${short_path}" >> "$OUTFILE"
    echo "  raw_url: ${raw_url}" >> "$OUTFILE"
    echo "  file_type: ${ext}" >> "$OUTFILE"
    echo "  description: ''" >> "$OUTFILE"
    echo "  tags: []" >> "$OUTFILE"
    echo "  last_updated: ${last_updated:-''}" >> "$OUTFILE"
    echo "  pod_owner: '${pod_owner}'" >> "$OUTFILE"
    echo "" >> "$OUTFILE"
done

echo "✅ memory_stub.yaml created at $OUTFILE"
