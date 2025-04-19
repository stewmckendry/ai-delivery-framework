# 📁 scripts/generate_patch.py
import argparse
import subprocess
import yaml
from pathlib import Path
from datetime import datetime

PATCH_DIR = Path(".patches")
PATCH_DIR.mkdir(parents=True, exist_ok=True)

METRICS_PATH = Path(".metrics/metrics.yaml")
CHANGELOG_PATH = Path(".logs/changelog.yaml")
THOUGHT_TRACE_PATH = Path(".logs/thought_trace.yaml")
HANDOFF_LOG_PATH = Path(".logs/handoff_log.yaml")

for log_path in [CHANGELOG_PATH, THOUGHT_TRACE_PATH, HANDOFF_LOG_PATH]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        with open(log_path, "w") as f:
            yaml.safe_dump([], f)

def get_git_diff():
    result = subprocess.run(["git", "diff", "--cached"], capture_output=True, text=True)
    return result.stdout.strip()

def get_changed_files():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    return result.stdout.strip().split("\n")

def determine_tags(files, patch_type):
    tags = set()
    if any("test" in f.lower() or "tests/" in f for f in files):
        tags.add("tests")
    if any("docs" in f.lower() or "readme" in f.lower() for f in files):
        tags.add("docs")
    if patch_type:
        tags.add(patch_type)
    return list(tags)

def update_metrics():
    print("[INFO] Metrics update triggered (stub).")

def write_patch_file(content, tags):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    patch_path = PATCH_DIR / f"patch_{ts}.diff"
    with open(patch_path, "w") as f:
        f.write(content)
    print(f"[OK] Patch saved: {patch_path}")
    print(f"[TAG] {', '.join(tags)}")

def append_to_log(log_path, entry):
    with open(log_path, "r") as f:
        data = yaml.safe_load(f) or []
    data.append(entry)
    with open(log_path, "w") as f:
        yaml.safe_dump(data, f)

def run_patch_validation():
    result = subprocess.run(["python", "scripts/validate_patch.py"])
    if result.returncode != 0:
        print("[FAIL] Patch validation failed.")
        exit(1)

def run_summary_generator():
    subprocess.run(["python", "scripts/generate_summary.py"])

def main():
    parser = argparse.ArgumentParser(description="Generate a Git patch with optional tagging")
    parser.add_argument("--update-metrics", action="store_true", help="Trigger metrics update after patch")
    parser.add_argument("--skip-log", action="store_true", help="Skip writing patch to .patches")
    parser.add_argument("--type", choices=["bug", "feature", "infra"], help="Type of patch work")
    parser.add_argument("--thought", type=str, help="Optional reasoning to include in the thought trace")
    parser.add_argument("--from-pod", type=str, default="dev", help="Pod handing off work")
    parser.add_argument("--to-pod", type=str, default="qa", help="Pod receiving work")
    parser.add_argument("--summary", action="store_true", help="Generate a markdown summary after patch")

    args = parser.parse_args()

    diff = get_git_diff()
    files = get_changed_files()

    if not diff:
        print("[WARN] No staged changes to commit.")
        return

    run_patch_validation()

    tags = determine_tags(files, args.type)

    ts = datetime.now().isoformat()

    if not args.skip_log:
        write_patch_file(diff, tags)

    if args.update_metrics:
        update_metrics()

    patch_entry = {
        "timestamp": ts,
        "files": files,
        "tags": tags,
        "type": args.type or "unspecified"
    }

    thought = args.thought or "Patch created with reasoning trace."
    handoff_entry = {
        "timestamp": ts,
        "from": args.from_pod,
        "to": args.to_pod,
        "reason": "Next pod in flow"
    }

    append_to_log(CHANGELOG_PATH, patch_entry)
    append_to_log(THOUGHT_TRACE_PATH, {"timestamp": ts, "thought": thought})
    append_to_log(HANDOFF_LOG_PATH, handoff_entry)

    if args.summary:
        run_summary_generator()

    print(f"[PR TAGS] Suggested: {', '.join(tags)}")

if __name__ == "__main__":
    main()