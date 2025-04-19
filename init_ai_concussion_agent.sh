#!/bin/bash
set -e

echo "🧠 Initializing AI Concussion Agent Project"

# 1. Clone or initialize Git
git init
git remote add origin https://github.com/stewmckendry/ai-concussion-agent.git
git checkout -b main

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

# 3. Create starter files
touch README.md .gitignore feature_backlog.yaml project_manifest.yaml

# 4. Download docs from delivery kit
docs_base="https://raw.githubusercontent.com/stewmckendry/ai-native-delivery/main"

docs_files=(
  "CONTRIBUTING.md"
  "docs/AI%20GitOps%20Setup%20Guide.md"
  "docs/AI-Native%20WoW%20SOP.md"
  "docs/Human%20Lead%20Role.md"
  "docs/Logs_Overview.md"
  "docs/Metrics%20Guide.md"
  "docs/POD_SOPs.md"
  "docs/ai_delivery_playbook.md"
  "docs/Handoff%20Template.md"
)

for file in "${docs_files[@]}"; do
  fname=$(basename "$file")
  curl -sSL "${docs_base}/${file}" -o "docs/ai-delivery-kit/${fname}"
done

# 5. Copy logs/
mkdir -p logs
curl -sSL https://raw.githubusercontent.com/stewmckendry/ai-native-delivery/main/logs/logs_template.yaml -o logs/logs_template.yaml
curl -sSL https://raw.githubusercontent.com/stewmckendry/ai-native-delivery/main/logs/metrics.yaml -o logs/metrics.yaml

# 6. Copy scripts/
mkdir -p scripts
curl -sSL https://raw.githubusercontent.com/stewmckendry/ai-native-delivery/main/scripts/generate_patch.py -o scripts/generate_patch.py
curl -sSL https://raw.githubusercontent.com/stewmckendry/ai-native-delivery/main/scripts/metrics_tracker.py -o scripts/metrics_tracker.py

echo "✅ Project initialized. Now run:"
echo "   git add . && git commit -m 'Init AI-native structure' && git push -u origin main"
