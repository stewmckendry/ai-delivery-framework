#!/bin/bash
set -e

echo "🧠 Initializing AI Concussion Agent Project (Full Delivery Kit)"

# 1. Init Git
git init
git remote add origin https://github.com/stewmckendry/ai-concussion-agent.git || true
git checkout -b main || git checkout main

# 2. Create folder structure
mkdir -p data \
         docs/ai-delivery-kit \
         logs \
         outputs \
         scripts \
         src/client \
         src/models \
         src/pods \
         src/server \
         src/utils \
         tests

# 3. Create key project files
touch README.md .gitignore feature_backlog.yaml project_manifest.yaml

# 4. Download all docs
echo "📥 Downloading docs..."
DOC_BASE="https://raw.githubusercontent.com/stewmckendry/ai-native-delivery/main"

docs_files=(
  "CONTRIBUTING.md"
  "docs/AI%20GitOps%20Setup%20Guide.md"
  "docs/AI%20GitOps%20WoW.md"
  "docs/AI%20Native%20Operating%20System%20(blog).md"
  "docs/AI-Native%20WoW%20Research.md"
  "docs/AI-Native%20WoW%20SOP.md"
  "docs/Burndown.md"
  "docs/Change_Log_Guide.md"
  "docs/Handoff%20Guide.md"
  "docs/Handoff%20Template.md"
  "docs/Handoff_Log_Guide.md"
  "docs/Human%20Lead%20Role.md"
  "docs/Logs_Overview.md"
  "docs/Metrics%20Guide.md"
  "docs/POD_CONTRIBUTING_Guide.md"
  "docs/POD_SOPs.md"
  "docs/README_detail.md"
  "docs/Retrospective.md"
  "docs/Summary_Report_Guide.md"
  "docs/Thought_Trace_Log.md"
  "docs/Velocity.md"
  "docs/ai_delivery_playbook.md"
  "docs/delivery_kit_maintenance.md"
  "docs/project_onboarding_guide.md"
  "docs/sop_delivery_pod.md"
  "docs/sop_dev_pod.md"
  "docs/sop_discovery_phase.md"
  "docs/sop_qa_pod.md"
  "docs/sop_research_pod.md"
  "docs/sop_wow_pod.md"
  "docs/transition_existing_projects.md"
  "docs/wow_templates_index.md"
)

for file in "${docs_files[@]}"; do
  fname=$(basename "$file")
  echo "📄 Downloading: $fname"
  curl -sSL "$DOC_BASE/$file" -o "docs/ai-delivery-kit/$fname"
done

# 5. Download logs
echo "📥 Downloading logs..."
LOG_BASE="$DOC_BASE/logs"

log_files=(
  "apply_patch.yaml"
  "apply_patch_enhanced.yaml"
  "metrics.yaml"
  "metrics_report_job.yaml"
)

for file in "${log_files[@]}"; do
  echo "📄 Downloading: $file"
  curl -sSL "$LOG_BASE/$file" -o "logs/$file"
done

# 6. Download scripts
echo "📥 Downloading scripts..."
SCRIPT_BASE="$DOC_BASE/scripts"

script_files=(
  "apply_patch.sh"
  "generate_patch.py"
  "generate_summary.py"
  "metrics_tracker.py"
  "scripts_run_discovery.sh"
  "scripts_run_tests.sh"
  "scripts_start_sprint.sh"
  "setup_ai_delivery.sh"
  "update_metrics_report.py"
  "validate_patch.py"
)

for file in "${script_files[@]}"; do
  echo "📄 Downloading: $file"
  curl -sSL "$SCRIPT_BASE/$file" -o "scripts/$file"
done

echo "✅ Project setup complete. Now run:"
echo "   git add . && git commit -m 'Init with full delivery kit' && git push -u origin main"
