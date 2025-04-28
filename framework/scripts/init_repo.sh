#!/bin/bash

# Rename existing repo (manual via GitHub Web UI advised)
echo "Please manually rename 'ai-delivery-framework' to 'ai-delivery-framework' via GitHub settings."
echo "\nWaiting 10 seconds for you to complete..."
sleep 10

# Create new PoC repo
NEW_REPO_NAME="nhl-predictor"
USER="stewmckendry"

# Use GitHub CLI (gh) to create repo
if gh repo view $USER/$NEW_REPO_NAME > /dev/null 2>&1; then
  echo "Repo $NEW_REPO_NAME already exists. Skipping creation."
else
  echo "Creating new repo: $NEW_REPO_NAME"
  gh repo create $USER/$NEW_REPO_NAME --public --confirm
fi

# Create project standard folders
mkdir -p project/data
mkdir -p project/notebooks
mkdir -p project/outputs/project_init
mkdir -p project/src/client
mkdir -p project/src/server
mkdir -p project/src/utils
mkdir -p project/src/scripts
mkdir -p project/docs
mkdir -p project/logs
mkdir -p project/test

# Also create empty /framework/ folder to be filled later by /project/init_project
#mkdir -p framework

# Touch basic placeholder files if necessary
touch project/outputs/.gitkeep

# Clone locally if needed
echo "\nTo clone locally:"
echo "git clone https://github.com/$USER/$NEW_REPO_NAME.git"
