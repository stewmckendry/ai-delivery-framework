# 📊 metrics_tracker.py
# Tool to track per-pod delivery activity and generate a summary metrics file

import os
import yaml
from datetime import datetime
from collections import defaultdict
from pathlib import Path

PATCH_DIR = Path(".patches")
METRICS_PATH = Path(".metrics/metrics.yaml")
os.makedirs(METRICS_PATH.parent, exist_ok=True)

# === Scan Patch Files ===
pod_counts = defaultdict(int)
feature_map = defaultdict(list)

for patch_file in PATCH_DIR.glob("*.diff"):
    name_parts = patch_file.stem.split("_")
    if len(name_parts) >= 3:
        feature_id = name_parts[2]
        pod = name_parts[-1]
        pod_counts[pod] += 1
        feature_map[pod].append(feature_id)

# === Load existing metrics if available ===
if METRICS_PATH.exists():
    with open(METRICS_PATH, "r") as f:
        existing = yaml.safe_load(f) or {}
else:
    existing = {}

# === Append current metrics snapshot ===
now = datetime.now().strftime("%Y-%m-%d %H:%M")
snapshot = {
    "timestamp": now,
    "patch_count": dict(pod_counts),
    "feature_ids": dict(feature_map)
}
existing[now] = snapshot

# === Save back to YAML ===
with open(METRICS_PATH, "w") as f:
    yaml.dump(existing, f, sort_keys=False)

print("✅ Metrics updated:")
for pod, count in pod_counts.items():
    print(f"- {pod}: {count} patches")
