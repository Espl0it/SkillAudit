#!/bin/bash
# Auto-push .openclaw to GitHub (for cron)

cd ~/.openclaw || exit 1

# Ensure SSH agent is running
if ! ssh-add -l >/dev/null 2>&1; then
    eval "$(ssh-agent -s)" >/dev/null
    ssh-add ~/.ssh/id_rsa 2>/dev/null
fi

# Check if there are any changes
if git diff --quiet && git diff --cached --quiet; then
    exit 0
fi

# Add all changes
git add -A

# Commit with timestamp
git commit -m "Auto-push $(date '+%Y-%m-%d %H:%M')" 2>/dev/null

# Push
git push origin master >> ~/.openclaw/logs/auto-push.log 2>&1
