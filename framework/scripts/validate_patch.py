# 📁 scripts/validate_patch.py
import subprocess

MANDATORY_TOUCH = ["tests", "docs"]


def get_git_diff():
    result = subprocess.run(["git", "diff", "--cached", "--name-only"], capture_output=True, text=True)
    files = result.stdout.strip().split("\n")
    return files

def validate_diff():
    files = get_git_diff()
    if not files:
        print("[FAIL] No staged files. Please stage your changes with `git add`.")
        return False

    touched = {key: any(key in f for f in files) for key in MANDATORY_TOUCH}

    for area, was_touched in touched.items():
        if not was_touched:
            print(f"[WARN] No {area} updated in this patch.")
        else:
            print(f"[OK] {area} changes detected.")

    print("[CHECK] Files staged:")
    for f in files:
        print(f" - {f}")
    return True

if __name__ == "__main__":
    validate_diff()