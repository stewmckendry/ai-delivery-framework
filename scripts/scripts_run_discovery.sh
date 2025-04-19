#!/bin/bash
echo "🔍 Running discovery phase..."
mkdir -p docs/discovery
touch docs/discovery/discovery_report.md
touch docs/research/research_log.md
cp docs/wow/templates/feature_backlog.yaml docs/wow/feature_backlog.yaml
cp docs/wow/templates/sprint_plan.yaml docs/wow/sprint_plan.yaml
echo "✅ Discovery artifacts initialized."