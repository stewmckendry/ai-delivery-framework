# 📊 update_metrics_report.py
# Parses metrics.yaml to update velocity.md and burndown.md summaries

import yaml
from pathlib import Path
from collections import defaultdict
from datetime import datetime

METRICS_PATH = Path(".metrics/metrics.yaml")
VELOCITY_PATH = Path(".metrics/velocity.md")
BURNDOWN_PATH = Path(".metrics/burndown.md")

if not METRICS_PATH.exists():
    print("⚠️ No metrics.yaml found. Run metrics_tracker.py first.")
    exit(1)

# === Load metrics snapshot ===
with open(METRICS_PATH, "r") as f:
    data = yaml.safe_load(f)

latest = list(data.values())[-1]
pod_counts = latest["patch_count"]
features = latest["feature_ids"]
timestamp = latest["timestamp"]

# === Update velocity.md ===
with open(VELOCITY_PATH, "w") as f:
    f.write(f"# 🚀 Pod Velocity – Patch Frequency & Feature Coverage\n\n")
    f.write(f"_This file is auto-updated by the metrics updater._\n\n")
    f.write(f"## 📅 Latest Summary: {timestamp}\n\n")
    f.write("| Pod       | Patches Submitted | Features Contributed |\n")
    f.write("|-----------|-------------------|------------------------|\n")
    for pod, count in pod_counts.items():
        feature_list = features.get(pod, [])
        f.write(f"| {pod: <10} | {count: <17} | {str(feature_list)} |\n")

# === Update burndown.md ===
delivered_features = sorted(set(f for lst in features.values() for f in lst))

with open(BURNDOWN_PATH, "w") as f:
    f.write("# 📉 Burndown – Feature Completion Status\n\n")
    f.write("_This file helps track open vs completed features over time._\n\n")
    f.write("## ✅ Delivered Features\n\n")
    for feat in delivered_features:
        f.write(f"- {feat}\n")
    f.write("\n## 🔧 In Progress / Unstarted Features\n\n")
    f.write("- (manually updated)\n\n")
    f.write("_Auto-generated from metrics.yaml_\n")

print("✅ Updated velocity.md and burndown.md from metrics.yaml")
