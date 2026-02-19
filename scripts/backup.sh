#!/bin/bash
# Backup workspace script
# Runs daily at 3 AM

BACKUP_DIR="${BACKUP_DIR:-/home/ecs-user/.openclaw/backups}"
WORKSPACE_DIR="/home/ecs-user/.openclaw/workspace"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Create backup filename
BACKUP_NAME="workspace_backup_${TIMESTAMP}.tar.gz"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Create backup
echo "[$(date)] Starting workspace backup..."
tar -czf "$BACKUP_PATH" -C "$(dirname "$WORKSPACE_DIR")" "$(basename "$WORKSPACE_DIR")" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "[$(date)] Backup created: $BACKUP_PATH"
    # Get backup size
    SIZE=$(du -h "$BACKUP_PATH" | cut -f1)
    echo "[$(date)] Backup size: $SIZE"
    
    # Keep only last 7 backups
    cd "$BACKUP_DIR" || exit 1
    ls -t workspace_backup_*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm -f
    echo "[$(date)] Old backups cleaned up"
else
    echo "[$(date)] ERROR: Backup failed!"
    exit 1
fi

echo "[$(date)] Backup completed successfully"
