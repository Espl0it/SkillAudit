# HEARTBEAT.md

# Heartbeat 定期检查任务
# 每次消息时会自动执行这些检查
# 采用智能告警：只在异常时告警，正常情况不打扰

## 定时任务

### 1. 检查 Git 仓库状态
- 描述: 检查 workspace 下的 git 仓库状态
- 命令: cd ~/.openclaw/workspace && git status --short
- 告警逻辑: **不告警** - 有未提交更改是正常情况（开发中）

### 2. 检查磁盘空间
- 描述: 检查磁盘空间是否充足
- 命令: df -h / | awk 'NR==2 {print "可用: " $4}'
- 告警逻辑: **磁盘使用率 > 90% 时才告警**
- 智能判断: 使用 `df / -1 | | tail awk '{print int(100-$5)}'` 获取可用百分比

### 3. 检查服务状态
- 描述: 检查 OpenClaw Gateway 是否正常运行
- 命令: openclaw gateway status
- 告警逻辑: **Gateway 不在 Running 状态时才告警**
- 智能判断: 检查状态输出中是否包含 "Running" 或 "running"

### 4. 清理临时文件
- 描述: 清理临时缓存文件
- 命令: find /tmp/openclaw* -mtime +7 -delete 2>/dev/null
- 告警逻辑: 不告警 - 后台清理任务

---

## 智能告警策略

| 检查项 | 阈值/条件 | 告警行为 |
|--------|-----------|----------|
| Git 仓库 | 有未提交更改 | **不告警**（正常开发状态） |
| 磁盘空间 | 使用率 > 90% | 告警 |
| Gateway 状态 | 非 Running | 告警 |
| 临时文件 | 超过 7 天 | 不告警（自动清理） |

## 实现建议

```python
# 伪代码示例
def check_heartbeat():
    results = {}
    
    # 1. Git 检查 - 不告警
    git_status = run("git status --short")
    results['git'] = git_status  # 记录但不告警
    
    # 2. 磁盘检查 - > 90% 才告警
    disk_usage = get_disk_usage()
    if disk_usage > 90:
        results['disk_alert'] = f"磁盘使用率 {disk_usage}% > 90%"
    
    # 3. Gateway 检查 - 不 Running 才告警
    gateway_status = get_gateway_status()
    if "Running" not in gateway_status:
        results['gateway_alert'] = f"Gateway 状态异常: {gateway_status}"
    
    return results
```
