#!/usr/bin/env python3

import os
import subprocess
import json
import datetime
from pathlib import Path
import argparse

def get_staged_diff():
    """Return the staged diff as a string."""
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def infer_output_folders_from_diff(diff_text):
    """Extract top-level folders from diff output."""
    folders = set()
    for line in diff_text.splitlines():
        if line.startswith("+++ b/"):
            path = line.replace("+++ b/", "").strip()
            if path:
                top_folder = path.split("/")[0]
                folders.add(top_folder)
    return sorted(folders)

def write_patch_file(diff_text, patch_file):
    with open(patch_file, "w") as f:
        f.write(diff_text)

def write_metadata_file(metadata, metadata_file):
    with open(metadata_file, "w") as f:
        json.dump(metadata, f, indent=2)

def main(task_id, summary):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    patch_name = f"patch_{timestamp}_{task_id}"
    patch_dir = Path(".patches")
    log_dir = Path(".logs/patches")
    patch_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    patch_path = patch_dir / f"{patch_name}.diff"
    metadata_path = log_dir / f"{patch_name}.json"

    # Step 1: Get staged diff
    diff_text = get_staged_diff()
    if not diff_text:
        print("⚠️ No staged changes found. Please stage files first.")
        return

    # Step 2: Infer folders from diff
    output_folders = infer_output_folders_from_diff(diff_text)

    # Step 3: Write .diff file
    write_patch_file(diff_text, patch_path)

    # Step 4: Write metadata
    metadata = {
        "patch_file": str(patch_path),
        "task_id": task_id,
        "summary": summary,
        "output_folders": output_folders
    }
    write_metadata_file(metadata, metadata_path)

    # Step 5: Confirm success
    print(f"✅ Patch created: {patch_path}")
    print(f"📝 Metadata saved: {metadata_path}")
    print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Git patch and metadata for an AI-native task.")
    parser.add_argument("--task_id", required=True, help="Task ID (e.g., 2.3_build_metrics_tool)")
    parser.add_argument("--summary", required=True, help="Short description of what this patch does")
    args = parser.parse_args()

    main(args.task_id, args.summary)
