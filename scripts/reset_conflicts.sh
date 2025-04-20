#!/bin/bash
set -e

echo "🧹 Resetting all staged and working changes..."
git reset --hard
git clean -fd
echo "✅ All local changes have been discarded. You can safely re-run the patch now."
