# MEMORY.md - Ada's Long-term Memory

## 工作区目录分类 (2026-02-19)

```
workspace/
├── projects/              # 独立项目
│   ├── SmartHome/         # 智能家居项目
│   ├── ReachyMini/        # 机器人项目
│   ├── fmp/               # 金融数据项目
│   └── OpenClawInstall/   # 安装脚本项目
│
├── skills/                # OpenClaw 技能 (系统)
│   └── [各种技能]
│
├── docs/                  # 文档/指南
│   ├── OpenClawGuide/     # OpenClaw 指南
│   ├── OpenCodeGuide/     # Code 指南
│   └── MakeSkillGuide/   # Skill 开发
│
├── config/                # 配置文件 (系统)
├── scripts/               # 脚本工具
├── memory/                # 记忆/日志 (系统)
├── cache/                 # 缓存
├── .agents/              # Agent 配置 (系统)
└── .openclaw/            # OpenClaw 内部 (系统)
```

---

## OpenClaw Skill 开发指南

### 目录结构
```
skill-name/
├── SKILL.md           # 必须：技能定义文件
├── scripts/           # 可选：脚本文件
├── references/        # 可选：参考文档
└── README.md         # 可选：详细说明
```

### SKILL.md 格式

**必须的 Frontmatter：**
```yaml
---
name: skill-name
description: 技能简短描述
---
```

**metadata 字段：**
- `emoji` - 技能图标
- `requires.bins` - 需要的命令行工具
- `requires.env` - 需要的环境变量
- `requires.config` - 需要的配置文件
- `primaryEnv` - 主环境变量名（API密钥）
- `os` - 支持的操作系统

### 技能加载位置
| 位置 | 路径 | 优先级 |
|------|------|--------|
| Workspace | `<project>/skills/` | 最高 |
| Managed | `~/.openclaw/skills/` | 中 |
| Bundled | 内置 | 最低 |

### 发布命令
```bash
# 本地安装
cp -r my-skill ~/.openclaw/skills/

# 通过 ClawHub 发布
clawhub publish

# 从 GitHub 安装
npx skills add https://github.com/username/skills.git --skill skill-name
```

### 参考资源
- 官方文档：https://docs.openclaw.ai/skills
- Awesome Skills：https://github.com/VoltAgent/awesome-openclaw-skills
- 中文技能库：https://github.com/clawdbot-ai/awesome-openclaw-skills-zh

---

## 已安装的 Skills

| Skill | 用途 |
|-------|------|
| tavily | AI 联网搜索 |
| weather | 天气查询 |
| github | GitHub 操作 |
| send-email | 发送邮件 |
| himalaya | 邮件管理 |
| tushare | 金融数据 |
| find-skills | 技能发现 |
| proactive-agent | 主动规划 |
| Dietitian | 膳食规划 |
| coding-agent | AI 编程助手 |

---

## API Tokens

- Tushare: `31c7a3335c9245deaec2bdc613531ab5ec794100df889e50353a31a9`
- Tavily: `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`

（实际使用时应从环境变量读取，不要硬编码）

---

## GitHub 仓库

- Aliyun-Ada (当前): git@github.com:Espl0it/Ada.git
- Aliyun-Eve (47.106.206.101): git@github.com:Espl0it/Eve.git

---

## 项目

- SmartHome: https://github.com/Espl0it/SmartHome
- OpenCodeGuide: https://github.com/Espl0it/OpenCodeGuide
- OpenClawGuide: https://github.com/Espl0it/OpenClawGuide
- MakeSkillGuide: https://github.com/Espl0it/MakeSkillGuide
- SkillAudit: https://github.com/Espl0it/SkillAudit

---

## Skill 安全审计

### 安装前审计流程 (方案1)

```bash
# 1. 克隆或下载 Skill（不直接安装）
npx clawhub install <skill> --dry-run  # 先查看信息

# 2. 审计 Skill
cd /tmp/<skill>
skill-audit /tmp/<skill>

# 3. 确认安全后安装
npx clawhub install <skill>
# 或
cp -r /tmp/<skill> ~/.openclaw/skills/
```

### 审计命令

```bash
# 审计指定 Skill
cd ~/.openclaw/workspace/skills/skill-audit
node scripts/scanner.js <skill路径>
```

### 审计规则

| 规则ID | 类型 | 说明 |
|--------|------|------|
| S001-S005 | secrets | 硬编码凭证 |
| C001-C005 | commands | 命令注入 |
| F001-F004 | files | 文件操作 |
| N001-N003 | network | 网络安全 |
| P001-P003 | permissions | 权限问题 |

### 严重等级

- 🔴 Critical - 立即处理
- 🟠 High - 尽快修复
- 🟡 Medium - 需要审查
- 🔵 Low - 轻微问题
- ℹ️ Info - 信息性
