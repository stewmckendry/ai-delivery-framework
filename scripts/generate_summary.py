# 📁 scripts/generate_summary.py
import yaml
from pathlib import Path
from datetime import datetime

LOGS_DIR = Path("logs")
HISTORY_DIR = Path("docs/history")
SUMMARY_INDEX = Path("docs/SUMMARY.md")

HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# Load logs
def load_yaml_log(filename):
    path = LOGS_DIR / filename
    if not path.exists():
        return []
    with open(path, "r") as f:
        return yaml.safe_load(f) or []

# Generate summary markdown from logs
thoughts = load_yaml_log("thought_trace.yaml")
changes = load_yaml_log("changelog.yaml")
handoffs = load_yaml_log("handoff_log.yaml")

now = datetime.now().strftime("%Y-%m-%d_%H%M")
summary_file = HISTORY_DIR / f"summary_{now}.md"

with open(summary_file, "w") as f:
    f.write(f"# 📅 Pod Summary - {now}\n\n")

    f.write("## 🧠 Thought Trace Highlights\n")
    for entry in thoughts[-10:]:
        f.write(f"- {entry['timestamp']}: {entry['thought']}\n")

    f.write("\n## 📒 Changelog Snapshots\n")
    for entry in changes[-10:]:
        files = ", ".join(entry.get("files", []))
        f.write(f"- {entry['timestamp']} ({entry['type']}): {files} [tags: {', '.join(entry.get('tags', []))}]\n")

    f.write("\n## 🔁 Handoff Log\n")
    for entry in handoffs[-10:]:
        f.write(f"- {entry['timestamp']}: {entry['from']} → {entry['to']} ({entry['reason']})\n")

# Update docs/SUMMARY.md
summary_line = f"- [{now}](history/summary_{now}.md)\n"
if not SUMMARY_INDEX.exists():
    with open(SUMMARY_INDEX, "w") as f:
        f.write("# 📃 Summary History\n\n")
        f.write(summary_line)
else:
    with open(SUMMARY_INDEX, "a") as f:
        f.write(summary_line)

print(f"[OK] Summary written to {summary_file}")