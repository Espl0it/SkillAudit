# Skill Audit

> OpenClaw Skill 安全审计工具

安全审计工具，用于检测 OpenClaw Skills 中的硬编码密钥、命令注入风险、文件操作漏洞等安全问题。

## 功能特性

- 🔒 **密钥检测 (Secrets)** - 检测硬编码的 API Key、Token、密码、私钥
- ⚠️ **命令注入 (Commands)** - 检测命令注入风险 (eval, exec, shell 执行)
- 📁 **文件安全 (Files)** - 文件路径遍历、可执行目录写入
- 🌐 **网络安全 (Network)** - 不安全的 HTTP、禁用的 SSL 验证
- 🔐 **权限分析 (Permissions)** - Skill 元数据中的过度权限

## 安装

Skill 已自动加载到 OpenClaw workspace，无需额外安装。

```bash
# 克隆项目（可选）
git clone https://github.com/Espl0it/SkillAudit.git

# 安装依赖
npm install

# 或复制到 OpenClaw Skills 目录
cp -r skill-audit ~/.openclaw/skills/
```

## 使用方法

### 基本审计

```bash
# 审计当前 workspace 中的所有 Skills
skill-audit

# 审计指定 Skill 目录
skill-audit /path/to/skill-directory

# 审计指定 Skill 文件
skill-audit /path/to/skill/SKILL.md
```

### 高级选项

```bash
# 仅审计特定规则类型
skill-audit --type secrets,commands

# 生成包含代码片段的详细输出
skill-audit --verbose

# 保存报告到文件
skill-audit --output audit-report.json

# 组合使用
skill-audit --type secrets,files --verbose --output report.json /path/to/skill
```

### 使用 audit.sh 脚本

```bash
# 审计所有 Skills
./scripts/audit.sh

# 审计指定目录
./scripts/audit.sh /path/to/skills
```

## 规则详解

### 密钥检测 (secrets)

检测硬编码的凭证：
- API keys 和 tokens
- 密码
- 私钥
- Base64 编码的密钥
- 云服务凭证

### 命令注入 (commands)

识别命令注入漏洞：
- 不安全的 eval() 和 Function() 使用
- 危险的 exec() 和 spawn() 调用
- Shell 命令拼接
- 子进程注入风险

### 文件操作 (files)

发现文件操作安全问题：
- 路径遍历漏洞
- 访问敏感系统文件
- 不安全的临时文件创建
- 写入可执行目录

### 网络安全 (network)

检测网络安全问题：
- 禁用 SSL 验证
- 使用不安全的 HTTP 协议
- 不安全的重定向处理

### 权限分析 (permissions)

分析 Skill 权限声明：
- 过度宽松的 "always: true" 权限
- 过度请求的环境变量
- 不必要的命令行工具要求

## 输出格式

工具生成以下结构的 JSON 报告：

```json
{
  "audit_time": "2024-01-01T00:00:00Z",
  "target": "/path/to/skill",
  "summary": {
    "total_issues": 5,
    "critical": 1,
    "high": 2,
    "medium": 1,
    "low": 1
  },
  "issues": [
    {
      "rule_id": "S001",
      "severity": "critical",
      "title": "硬编码 API Key/Token",
      "file": "scripts/api.js",
      "line": 42,
      "code": "const apiKey = 'sk-xxx...'",
      "recommendation": "使用环境变量或安全凭证存储"
    }
  ]
}
```

## 严重等级

- 🔴 **Critical (严重)** - 需要立即处理的安全风险
- 🟠 **High (高)** - 重要的安全漏洞，应尽快修复
- 🟡 **Medium (中)** - 中等安全问题，需要审查
- 🔵 **Low (低)** - 轻微安全问题或最佳实践违规
- ℹ️ **Info (信息)** - 信息性发现

## 最佳实践

1. **定期审计** - 开发过程中定期运行审计
2. **提交前检查** - 集成到开发工作流程
3. **及时修复** - 立即处理严重和高危问题
4. **验证确认** - 修复后重新审计确认问题已解决

## 局限性

- 仅限静态分析（无运行时行为分析）
- 可能产生误报
- 仅支持有限语言（JavaScript、Python、Bash）
- 不检查外部依赖项的漏洞

## 自定义规则

在 `scripts/rules/` 目录下添加新的 YAML 规则文件：

- `secrets.yaml` - 密钥检测规则
- `commands.yaml` - 命令注入规则
- `files.yaml` - 文件操作规则
- `network.yaml` - 网络安全规则
- `permissions.yaml` - 权限规则

## 与 OpenClaw 集成

在 OpenClaw 中直接使用：

```
# 告诉 Ada
"审计 tavily-search skill"
```

## License

MIT

## 相关链接

- GitHub: https://github.com/Espl0it/SkillAudit
- OpenClaw 文档: https://docs.openclaw.ai
