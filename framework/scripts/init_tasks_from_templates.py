#!/usr/bin/env python3

"""
Initialize the master task.yaml by merging all task.yaml files
found under task_templates/**/task.yaml.

Run from the project root:
> python scripts/init_tasks_from_templates.py

Pre-requisites:
- `task_templates/` folder with subfolders per phase, each containing a task.yaml
- PyYAML installed (`pip install pyyaml`)
"""

import os
import glob
import yaml
from datetime import datetime

TEMPLATE_GLOB = "task_templates/**/task.yaml"
OUTPUT_PATH = "task.yaml"

def load_yaml(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def write_yaml(path, data):
    with open(path, "w") as f:
        yaml.dump(data, f, sort_keys=False)

def main():
    print("🔄 Initializing master task.yaml from task templates...")
    all_tasks = {}

    for path in glob.glob(TEMPLATE_GLOB, recursive=True):
        task_data = load_yaml(path)
        for task_id, task in task_data.get("tasks", {}).items():
            if task_id in all_tasks:
                print(f"⚠️ Warning: duplicate task ID {task_id} from {path}")
            task["status"] = "backlog"
            task["done"] = False
            task["assigned_to"] = "unassigned"
            task["instance_of"] = path
            task["created_at"] = datetime.now().isoformat()
            task["updated_at"] = datetime.now().isoformat()
            all_tasks[task_id] = task
            print(f"✅ Added: {task_id} from {path}")

    # Sort by task_id
    sorted_tasks = dict(sorted(all_tasks.items()))
    write_yaml(OUTPUT_PATH, {"tasks": sorted_tasks})
    print(f"🎉 Done! Master task list written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
