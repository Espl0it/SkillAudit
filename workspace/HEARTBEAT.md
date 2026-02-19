# HEARTBEAT.md

# Heartbeat 定期检查任务
# 每次消息时会自动执行这些检查

## 定时任务

### 1. 检查 Git 仓库状态
- 描述: 检查 workspace 下的 git 仓库状态
- 命令: cd ~/.openclaw/workspace && git status --short

### 2. 检查磁盘空间
- 描述: 检查磁盘空间是否充足
- 命令: df -h / | awk 'NR==2 {print "可用: " $4}'

### 3. 检查服务状态
- 描述: 检查 OpenClaw Gateway 是否正常运行
- 命令: openclaw status 2>&1 | grep -E "Gateway|Status"

### 4. 清理临时文件
- 描述: 清理临时缓存文件
- 命令: find /tmp/openclaw* -mtime +7 -delete 2>/dev/null
