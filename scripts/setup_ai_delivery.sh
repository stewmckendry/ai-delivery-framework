#!/bin/bash
# 📦 setup_ai_delivery.sh
# One-shot setup script for AI-Native Delivery repo

set -e  # Exit on error

# === CONFIG ===
REPO_NAME="ai-native-delivery"
REPO_URL="https://github.com/stewmckendry/$REPO_NAME.git"
PATCH_BRANCH="chatgpt/dev/f4.3_rtp_guidance"
PATCH_FILE="gpt_patch_f4.3.diff"

# === FOLDER SETUP ===
echo "📁 Creating folder structure..."
mkdir -p $REPO_NAME/.github/workflows
mkdir -p $REPO_NAME/.patches
mkdir -p $REPO_NAME/scripts

# === GITHUB ACTION ===
echo "⚙️ Writing GitHub Action..."
cat << 'EOF' > $REPO_NAME/.github/workflows/apply_patch_enhanced.yaml
name: 🧠 Enhanced GPT Patch Flow

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

      - name: Create Feature Branch
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
          get_or_default() { [ -f "$1" ] && echo "$(cat $1)" || echo "_Not provided._"; }
          echo "changelog<<EOF" >> $GITHUB_OUTPUT
          get_or_default docs/changelog.md >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "trace<<EOF" >> $GITHUB_OUTPUT
          get_or_default logs/thought_trace.md >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

          echo "handoff<<EOF" >> $GITHUB_OUTPUT
          get_or_default docs/wow/handoff_log.yaml >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          branch: chatgpt/auto/${{ steps.detect.outputs.patch_name }}
          title: "🤖 GPT Patch: ${{ steps.detect.outputs.patch_name }}"
          commit-message: "Auto-applied patch and opened PR"
          body: |
            This PR was generated automatically from `${{ steps.detect.outputs.patch_file }}`.

            ## 📒 Changelog
            ${{ steps.logs.outputs.changelog }}

            ## 🧠 Thought Trace
            ${{ steps.logs.outputs.trace }}

            ## 🔁 Handoff Log
            ${{ steps.logs.outputs.handoff }}

            Please review and merge if appropriate.
EOF

# === SAMPLE PATCH ===
echo "🧠 Adding example patch file..."
cat << 'EOF' > $REPO_NAME/.patches/$PATCH_FILE
diff --git a/src/models/guidance_generator.py b/src/models/guidance_generator.py
new file mode 100644
index 0000000..abcdef0
--- /dev/null
+++ b/src/models/guidance_generator.py
@@
+# F4.3 - Return-to-Play Guidance Generator
+def generate_guidance(symptoms, protocol_data):
+    """Return basic RTP guidance based on symptom status."""
+    if not symptoms:
+        return "Please complete the symptom checklist to receive tailored advice."
+    return "Based on your symptoms, we recommend starting at Stage 2 of Return-to-Play."
EOF

# === PATCH APPLIER ===
echo "🛠️ Writing patch apply script..."
cat << 'EOF' > $REPO_NAME/scripts/apply_patch_enhanced.sh
#!/bin/bash
set -e
REPO="$REPO_NAME"
PATCH_FILE="$1"

if [ -z "$PATCH_FILE" ]; then
  echo "❌ Usage: ./scripts/apply_patch_enhanced.sh <patch-file.diff>"
  exit 1
fi

cd $REPO
BRANCH="chatgpt/dev/$(basename $PATCH_FILE .diff)"
git checkout -b "$BRANCH"
patch -p1 < "../.patches/$PATCH_FILE"
git add .
git commit -m "[AutoPatch] Apply $PATCH_FILE"
git push origin "$BRANCH"
EOF
chmod +x $REPO_NAME/scripts/apply_patch_enhanced.sh

# === FINAL MESSAGE ===
echo "✅ Setup complete!"
echo "➡️ Next: cd $REPO_NAME && git init && git remote add origin $REPO_URL"
echo "Then: git add . && git commit -m 'Initial setup' && git push -u origin main"
