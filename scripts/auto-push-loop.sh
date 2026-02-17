#!/bin/bash
# Auto-push .openclaw to GitHub (loop version)

cd ~/.openclaw || exit 1

# Ensure SSH agent is running
if ! ssh-add -l >/dev/null 2>&1; then
    eval "$(ssh-agent -s)" >/dev/null
    ssh-add ~/.ssh/id_rsa 2>/dev/null
fi

while true; do
    # Check if there are any changes
    if git diff --quiet && git diff --cached --quiet; then
        sleep 300  # 5 minutes
        continue
    fi

    # Add all changes
    git add -A

    # Commit with timestamp
    git commit -m "Auto-push $(date '+%Y-%m-%d %H:%M')" 2>/dev/null

    # Push
    if git push origin master 2>&1; then
        echo "Pushed at $(date)"
    else
        echo "Push failed at $(date)"
    fi

    sleep 300  # 5 minutes
done
