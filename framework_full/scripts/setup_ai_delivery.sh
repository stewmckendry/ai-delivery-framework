#!/bin/bash
set -e

echo "🧠 Setting up AI-native delivery automation..."

# Ensure folders exist
mkdir -p .github/workflows
mkdir -p .patches
mkdir -p logs
mkdir -p docs

# Write GitHub Action that auto-applies .diff patches
echo "⚙️ Creating GitHub Action: .github/workflows/apply_patch_enhanced.yaml"

cat << 'EOF' > .github/workflows/apply_patch_enhanced.yaml
name: Enhanced GPT Patch Flow

on:
  push:
    paths:
      - '.patches/*.diff'

jobs:
  apply-and-pr:
    runs-on: ubuntu-latest
    name: Apply Patch + Create Rich PR

    steps:
      - name: Checkout Repo
        uses: actions/checkout@v3

      - name: Set Git Config
        run: |
          git config --global user.name "chatgpt-bot"
          git config --global user.email "chatgpt-bot@users.noreply.github.com"

      - name: Detect Patch File
        id: detect
        run: |
          PATCH_FILE=$(find .patches -name '*.diff' | head -n 1)
          PATCH_NAME=$(basename "$PATCH_FILE" .diff)
          echo "patch_file=$PATCH_FILE" >> $GITHUB_OUTPUT
          echo "patch_name=$PATCH_NAME" >> $GITHUB_OUTPUT

      - name: Create Feature Branch and Apply Patch
        run: |
          BRANCH=chatgpt/auto/${{ steps.detect.outputs.patch_name }}
          git checkout -b "$BRANCH"
          patch -p1 < "${{ steps.detect.outputs.patch_file }}"
          git add .
          git commit -m "[AutoPatch] Apply ${{ steps.detect.outputs.patch_name }}"
          git push origin "$BRANCH"

      - name: Extract Log Content (if present)
        id: logs
        run: |
          get_or_default() { [ -f "$1" ] && cat "$1" || echo "_Not provided._"; }
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          get_or_default docs/changelog.md >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
          echo "trace<<EOF" >> $GITHUB_OUTPUT
          get_or_default logs/thought_trace.md >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Open Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: \${{ secrets.GITHUB_TOKEN }}
          branch: chatgpt/auto/${{ steps.detect.outputs.patch_name }}
          title: "📦 Patch: ${{ steps.detect.outputs.patch_name }}"
          body: |
            ## 🧠 AI-Native Patch: \`${{ steps.detect.outputs.patch_name }}\`

            ### 📄 Changelog
            ${{ steps.logs.outputs.changelog }}

            ### 🧠 Thought Trace
            ${{ steps.logs.outputs.trace }}

            _Patch created automatically from .patches folder._
EOF

echo "✅ AI Delivery GitHub Action installed!"
