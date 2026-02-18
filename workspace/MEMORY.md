# MEMORY.md - Ada's Long-term Memory

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
