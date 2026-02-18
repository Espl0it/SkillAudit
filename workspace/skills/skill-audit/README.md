# Skill Audit

> OpenClaw Skill 安全审计工具

安全审计工具，用于检测 OpenClaw Skills 中的硬编码密钥、命令注入风险、文件操作漏洞等问题。

## 功能

- 🔒 **Secrets Detection** - 检测硬编码的 API Key、Token、密码
- ⚠️ **Command Injection** - 检测命令注入风险 (eval, exec, shell 执行)
- 📁 **File Security** - 文件路径遍历、可执行目录写入
- 🌐 **Network Security** - 不安全的 HTTP、禁用的 SSL 验证
- 🔐 **Permission Analysis** - Skill 元数据中的过度权限

## 支持的语言

- JavaScript/Node.js
- Python
- Bash 脚本

## 安装

```bash
# 克隆项目
git clone https://github.com/Espl0it/SkillAudit.git
cd SkillAudit

# 安装依赖
npm install

# 或作为 OpenClaw Skill 安装
cp -r skill-audit ~/.openclaw/skills/
```

## 使用方法

### 命令行

```bash
# 审计当前目录的所有 Skills
node scripts/scanner.js

# 审计指定 Skill
node scripts/scanner.js /path/to/skill

# 审计特定规则类型
node scripts/scanner.js --type secrets,commands

# 生成详细报告
node scripts/scanner.js --verbose --output report.json
```

### 使用 audit.sh 脚本

```bash
# 审计所有 Skills
./scripts/audit.sh

# 审计指定目录
./scripts/audit.sh /path/to/skills
```

## 规则类型

| 规则ID | 类型 | 说明 |
|--------|------|------|
| S001-S005 | secrets | 硬编码凭证 |
| C001-C005 | commands | 命令注入风险 |
| F001-F004 | files | 文件操作漏洞 |
| N001-N003 | network | 网络安全问题 |
| P001-P003 | permissions | 权限问题 |

## 输出示例

```json
{
  "audit_time": "2026-02-18T10:00:00.000Z",
  "target": "/path/to/skill",
  "summary": {
    "total_issues": 2,
    "critical": 0,
    "high": 2,
    "medium": 0,
    "low": 0
  },
  "issues": [
    {
      "rule_id": "S001",
      "severity": "high",
      "title": "Hardcoded API Key",
      "file": "scripts/api.js",
      "line": 10,
      "recommendation": "Use environment variables instead"
    }
  ]
}
```

## 配置文件

编辑 `scripts/rules/` 下的 YAML 文件自定义规则：

- `secrets.yaml` - 密钥检测规则
- `commands.yaml` - 命令注入规则
- `files.yaml` - 文件操作规则
- `network.yaml` - 网络安全规则
- `permissions.yaml` - 权限规则

## 与 OpenClaw 集成

在 OpenClaw 中使用：

```
# 告诉 Ada
"审计 tavily-search skill"
```

## License

MIT
