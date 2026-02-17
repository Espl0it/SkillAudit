#!/bin/bash
# Auto-push .openclaw to GitHub

cd ~/.openclaw || exit 1

# Check if there are any changes
if git diff --quiet && git diff --cached --quiet; then
    exit 0
fi

# Add all changes
git add -A

# Commit with timestamp
git commit -m "Auto-push $(date '+%Y-%m-%d %H:%M')" 2>/dev/null

# Push
git push origin master 2>&1
