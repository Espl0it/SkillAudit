#!/bin/bash
# Log cleanup script
# Runs daily at 2 AM - removes logs older than 7 days

LOG_DIR="${LOG_DIR:-/home/ecs-user/.openclaw/logs}"
DAYS_TO_KEEP=7

echo "[$(date)] Starting log cleanup..."

# Check if log directory exists
if [ ! -d "$LOG_DIR" ]; then
    echo "[$(date)] Log directory does not exist: $LOG_DIR"
    exit 0
fi

# Count files before cleanup
BEFORE_COUNT=$(find "$LOG_DIR" -type f 2>/dev/null | wc -l)

# Find and delete files older than DAYS_TO_KEEP
find "$LOG_DIR" -type f -mtime +$DAYS_TO_KEEP -delete 2>/dev/null

# Count files after cleanup
AFTER_COUNT=$(find "$LOG_DIR" -type f 2>/dev/null | wc -l)
DELETED_COUNT=$((BEFORE_COUNT - AFTER_COUNT))

echo "[$(date)] Cleanup completed: deleted $DELETED_COUNT old log files"

# Also clean up any old backup files (keep last 7)
BACKUP_DIR="${BACKUP_DIR:-/home/ecs-user/.openclaw/backups}"
if [ -d "$BACKUP_DIR" ]; then
    find "$BACKUP_DIR" -type f -mtime +$DAYS_TO_KEEP -delete 2>/dev/null
    echo "[$(date)] Old backups cleaned up"
fi

echo "[$(date)] Log cleanup finished"
