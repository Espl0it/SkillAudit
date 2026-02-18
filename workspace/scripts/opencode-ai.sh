#!/bin/bash
# OpenCode Automation Script
# Usage: ./opencode-ai.sh "Your prompt here"

export PATH="/home/ecs-user/.opencode/bin:$PATH"

# Create a temporary file for the session
SESSION_DIR="/tmp/opencode-sessions/$$"
mkdir -p "$SESSION_DIR"

# Run opencode with the prompt
cd "$SESSION_DIR"
echo "$1" | opencode --dir /home/ecs-user/.openclaw/workspace --yes 2>&1 | head -100

# Cleanup
rm -rf "$SESSION_DIR"
