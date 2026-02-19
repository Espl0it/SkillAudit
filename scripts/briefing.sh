#!/bin/bash
# Morning briefing script
# Runs daily at 7 AM - generates daily briefing and sends to Feishu

WORKSPACE_DIR="/home/ecs-user/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE_DIR/memory"
TODAY=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

echo "[$(date)] Generating morning briefing..."

# Start building the briefing
BRIEFING="🌅 **晨间简报 - ${TODAY}**\n\n"

# Add date info
BRIEFING+="📅 日期: ${TODAY}\n"
BRIEFING+="⏰ 生成时间: $(date +%H:%M)\n\n"

# Add memory summary from yesterday and today
BRIEFING+="📝 **近期动态**\n"

for day in $YESTERDAY $TODAY; do
    MEMORY_FILE="${MEMORY_DIR}/${day}.md"
    if [ -f "$MEMORY_FILE" ]; then
        BRIEFING+="\n### ${day}\n"
        # Get first 500 chars of memory file
        CONTENT=$(head -c 500 "$MEMORY_FILE" 2>/dev/null)
        BRIEFING+="${CONTENT}\n"
    fi
done

# Add workspace status
BRIEFING+="\n📁 **工作区状态**\n"
if [ -d "$WORKSPACE_DIR" ]; then
    FILE_COUNT=$(find "$WORKSPACE_DIR" -type f 2>/dev/null | wc -l)
    DIR_COUNT=$(find "$WORKSPACE_DIR" -type d 2>/dev/null | wc -l)
    BRIEFING+="- 文件数: ${FILE_COUNT}\n"
    BRIEFING+="- 目录数: ${DIR_COUNT}\n"
fi

# Add system info
BRIEFING+="\n💻 **系统信息**\n"
BRIEFING+="- 主机: $(hostname)\n"
BRIEFING+="- 运行时间: $(uptime -p 2>/dev/null || uptime)\n"

# Add today's reminder
BRIEFING+="\n✨ **今日提醒**\n"
BRIEFING+="- 记得查看待办事项\n"
BRIEFING+="- 检查日程安排\n"

BRIEFING+="\n---\n"
BRIEFING+="*此简报由 OpenClaw 自动生成*"

echo "[$(date)] Briefing generated, sending to Feishu..."

# Send to Feishu using OpenClaw message command
# The message will be sent to the default channel (feishu)
openclaw message send --channel feishu --message "$BRIEFING" 2>&1

if [ $? -eq 0 ]; then
    echo "[$(date)] Briefing sent successfully to Feishu"
else
    echo "[$(date)] WARNING: Failed to send to Feishu, trying alternative..."
    # Try sending to the main session
    openclaw message send --message "$BRIEFING" 2>&1
fi

echo "[$(date)] Morning briefing completed"
