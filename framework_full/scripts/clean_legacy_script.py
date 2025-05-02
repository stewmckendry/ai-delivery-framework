import os
import shutil
import subprocess
from pathlib import Path

# --- CONFIG ---
PATCH_DIR = Path(".patches")
ARCHIVE_DIR = Path("archive/patches")
PATCH_PATTERN = "patch_*.diff"


def archive_patch_files():
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    patch_files = list(PATCH_DIR.glob(PATCH_PATTERN))
    if not patch_files:
        print("✅ No patch files to archive.")
        return

    for file in patch_files:
        target = ARCHIVE_DIR / file.name
        print(f"📦 Archiving {file} → {target}")
        shutil.move(str(file), str(target))


def delete_remote_patch_branches():
    print("\n🧹 Deleting remote branches matching 'chatgpt/auto/patch_*'...")
    try:
        # List remote branches
        result = subprocess.run(
            ["git", "branch", "-r"], capture_output=True, text=True, check=True
        )
        branches = result.stdout.splitlines()
        patch_branches = [
            b.strip().replace("origin/", "")
            for b in branches
            if b.strip().startswith("origin/chatgpt/auto/patch_")
        ]

        for branch in patch_branches:
            print(f"❌ Deleting remote branch: {branch}")
            subprocess.run(["git", "push", "origin", "--delete", branch])

    except subprocess.CalledProcessError as e:
        print("❌ Error listing or deleting remote branches:", e)


if __name__ == "__main__":
    archive_patch_files()
    delete_remote_patch_branches()
    print("\n✅ Cleanup complete.")
