import os
import sys
import subprocess
import argparse
import yaml
from datetime import datetime
from pathlib import Path

# Constants
PATCH_DIR = Path(".patches")
LOG_DIR = Path(".logs")
PATCH_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

CHANGELOG_PATH = LOG_DIR / "changelog.yaml"
HANDOFF_LOG_PATH = LOG_DIR / "handoff_log.yaml"
THOUGHT_TRACE_PATH = LOG_DIR / "thought_trace.yaml"

# Helpers to write logs
def append_to_log(path, new_entry):
    if path.exists():
        with open(path, "r") as f:
            data = yaml.safe_load(f) or []
    else:
        data = []
    data.append(new_entry)
    with open(path, "w") as f:
        yaml.dump(data, f)

def slugify(text):
    return text.lower().replace(" ", "_").replace("/", "-")[:50]

def generate_patch_name():
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"patch_{ts}"

def create_diff(patch_name):
    patch_path = PATCH_DIR / f"{patch_name}.diff"
    with open(patch_path, "w") as f:
        subprocess.run(["git", "diff", "--cached"], stdout=f)
    return patch_path

def main():
    parser = argparse.ArgumentParser(description="Generate a patch and supporting logs for a GPT contribution.")
    parser.add_argument("--type", required=True, help="Type of patch: fix, feature, tests, docs")
    parser.add_argument("--thought", required=True, help="Summary of the idea, fix, or feature")
    parser.add_argument("--autopromote", action="store_true", help="Auto-run patch promotion script after generation")
    args = parser.parse_args()

    # Auto-stage unstaged files (new or modified)
    unstaged_files = subprocess.run(
        ["git", "ls-files", "--others", "--modified", "--exclude-standard"],
        stdout=subprocess.PIPE,
        text=True
    ).stdout.strip().splitlines()

    if unstaged_files:
        print(f"[AUTO] Adding {len(unstaged_files)} unstaged file(s):")
        for f in unstaged_files:
            print(f"  - {f}")
            subprocess.run(["git", "add", f])

    # Check for staged files
    result = subprocess.run(["git", "diff", "--cached", "--name-only"],
                            stdout=subprocess.PIPE, text=True)
    staged_files = result.stdout.strip().splitlines()

    if not staged_files:
        print("[WARN] No staged changes to commit.")
        return

    for f in staged_files:
        if f.startswith("tests/"):
            print("[TAG] Test file detected")
        if f.startswith("docs/"):
            print("[TAG] Docs update detected")
        print(f"[CHECK] Files staged:\n - {f}")

    # Generate patch
    patch_name = generate_patch_name()
    patch_path = create_diff(patch_name)
    print(f"[OK] Patch saved: {patch_path}")

    # Tagging info
    tags = [args.type]
    if any("test" in f for f in staged_files):
        tags.append("tests")
    if any("doc" in f for f in staged_files):
        tags.append("docs")
    print(f"[TAG] {', '.join(tags)}")

    # Save to logs
    changelog_entry = {
        "patch": patch_name,
        "type": args.type,
        "files": staged_files,
        "thought": args.thought,
        "tags": tags,
        "timestamp": datetime.now().isoformat(),
    }
    append_to_log(CHANGELOG_PATH, changelog_entry)

    thought_entry = {
        "thought": args.thought,
        "timestamp": datetime.now().isoformat(),
        "files": staged_files,
    }
    append_to_log(THOUGHT_TRACE_PATH, thought_entry)

    handoff_entry = {
        "patch": patch_name,
        "promoted": args.autopromote,
        "files": staged_files,
        "tags": tags,
        "timestamp": datetime.now().isoformat(),
    }
    append_to_log(HANDOFF_LOG_PATH, handoff_entry)

    if args.autopromote:
        print("🧠 Starting AI-native patch promotion to feature branch...")
        subprocess.run(["bash", "scripts/create_pr_from_patch.sh"])
    else:
        print("🚀 Done generating patch. Run 'scripts/create_pr_from_patch.sh' to promote it.")

if __name__ == "__main__":
    main()
