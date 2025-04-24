#!/bin/bash
set -e

echo "🧹 Pruning stale remote tracking branches..."
git fetch --prune

BRANCHES_TO_DELETE=$(git branch --merged main | grep -v '\*' | grep 'chatgpt/auto/')
if [ -z "$BRANCHES_TO_DELETE" ]; then
    echo "✅ No local branches to delete."
else
    echo "$BRANCHES_TO_DELETE" | xargs -n 1 echo "🌿 Candidate for deletion: "
    read -p "Do you want to delete these branches? (y/n): " confirm
    if [ "$confirm" = "y" ]; then
        echo "$BRANCHES_TO_DELETE" | xargs -n 1 git branch -d
        echo "🗑️ Deleted branches."
    else
        echo "No branches were deleted."
    fi
fi

REMOTE_BRANCHES_TO_DELETE=$(git branch -r --merged main | grep 'chatgpt/auto/' | sed 's/origin\///')
if [ -z "$REMOTE_BRANCHES_TO_DELETE" ]; then
    echo "✅ No remote branches to delete."
else
    echo "$REMOTE_BRANCHES_TO_DELETE" | xargs -n 1 echo "🌍 Remote branch candidate: "
    read -p "Do you want to delete the corresponding remote branches? (y/n): " remote_confirm
    if [ "$remote_confirm" = "y" ]; then
        echo "$REMOTE_BRANCHES_TO_DELETE" | xargs -n 1 git push origin --delete
        echo "🗑️ Deleted remote branches."
    else
        echo "No remote branches were deleted."
    fi
fi

echo "✅ Done. Use \`git branch -vv\` to verify local branches."
