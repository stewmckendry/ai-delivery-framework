#!/bin/bash
echo "🚀 Starting new sprint..."
mkdir -p docs/status
touch docs/status/weekly_report.md
cp docs/wow/templates/sprint_plan.yaml docs/wow/sprint_plan.yaml
cp docs/wow/templates/handoff_log.yaml docs/wow/handoff_log.yaml
echo "✅ Sprint plan and logs initialized."