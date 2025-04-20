import os
import sys
import argparse
import subprocess
import difflib
import yaml
from datetime import datetime
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
PATCHES_DIR = PROJECT_ROOT / ".patches"
LOGS_DIR = PROJECT_ROOT / ".logs"
PATCHES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

CHANGELOG_PATH = LOGS_DIR / "changelog.yaml"
HANDOFF_LOG_PATH = LOGS_DIR / "handoff_log.yaml"
THOUGHT_TRACE_PATH = LOGS_DIR / "thought_trace.yaml"


def get_staged_files():
    result = subprocess.run(["git", "diff", "--name-only", "--cached"], capture_output=True, text=True)
    return result.stdout.strip().split("\n") if result.stdout else []


def file_exists_in_repo(file_path):
    result = subprocess.run(["git", "ls-files", file_path], capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip() != ""


def generate_diff(staged_files, patch_path):
    with open(patch_path, "w") as patch_file:
        for file in staged_files:
            subprocess.run(["git", "diff", "--cached", file], stdout=patch_file)


def append_to_log(log_path, entry):
    if not log_path.exists():
        with open(log_path, "w") as f:
            yaml.dump([], f)
    with open(log_path, "r") as f:
        data = yaml.safe_load(f) or []
    data.append(entry)
    with open(log_path, "w") as f:
        yaml.dump(data, f)


def check_merge_conflict_risk(staged_files):
    risky_files = []
    for file in staged_files:
        if file_exists_in_repo(file):
            risky_files.append(file)
    return risky_files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, help="Type of patch: bugfix, feature, tests")
    parser.add_argument("--thought", required=True, help="Thought or purpose behind the patch")
    parser.add_argument("--autopromote", action="store_true", help="Promote patch immediately")
    args = parser.parse_args()

    staged_files = get_staged_files()
    if not staged_files:
        print("[WARN] No staged changes to commit.")
        sys.exit(0)

    risky_files = check_merge_conflict_risk(staged_files)
    if risky_files:
        print("⚠️ POTENTIAL MERGE CONFLICT: These files already exist in the repo and are staged:")
        for f in risky_files:
            print(f"  - {f}")
        print("👉 Consider running './scripts/reset_conflicts.sh' to discard or unstage.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    patch_filename = f"patch_{timestamp}.diff"
    patch_path = PATCHES_DIR / patch_filename

    generate_diff(staged_files, patch_path)
    print("[OK] Patch saved:", patch_path)

    # Thought tag heuristics
    tags = [args.type]
    if any("test" in f.lower() for f in staged_files):
        tags.append("tests")
    print("[TAG]", ", ".join(set(tags)))

    # Log entries
    changelog_entry = {
        "timestamp": timestamp,
        "type": args.type,
        "files": staged_files,
        "patch": str(patch_path)
    }
    thought_entry = {
        "timestamp": timestamp,
        "thought": args.thought,
        "files": staged_files,
        "tags": tags
    }
    handoff_entry = {
        "timestamp": timestamp,
        "patch_file": str(patch_path),
        "branch_name": f"chatgpt/auto/{patch_filename[:-5]}",
        "status": "generated"
    }

    append_to_log(CHANGELOG_PATH, changelog_entry)
    append_to_log(THOUGHT_TRACE_PATH, thought_entry)
    append_to_log(HANDOFF_LOG_PATH, handoff_entry)

    if args.autopromote:
        print("🧠 Starting AI-native patch promotion to feature branch...")
        subprocess.run(["bash", str(PROJECT_ROOT / "scripts" / "create_pr_from_patch.sh")])


if __name__ == "__main__":
    main()
