# Alex 项目重新规划方案

> 基于 xiaomo.dev 设计理念，为 Ada (OpenClaw AI 助手) 打造的个人主页

---

## 项目概述

**项目名称**: Alex 个人主页  
**定位**: 展示 AI 助手功能、日常工作和技能的展示网站  
**参考**: xiaomo.dev  
**目标用户**: 对 AI Agent 感兴趣的技术爱好者、潜在用户

---

## 页面结构

```
alex-home/
├── public/
│   ├── index.html          # 单页应用入口
│   ├── styles/
│   │   └── main.css      # 样式文件
│   └── assets/
│       └── logo.svg       # Logo
├── src/
│   ├── components/       # React/Vue 组件
│   ├── pages/           # 页面组件
│   ├── hooks/           # 自定义 Hooks
│   └── utils/           # 工具函数
├── api/                 # 后端 API (可选)
├── README.md
└── package.json
```

---

## 页面内容规划

### 1. 首页 (Hero Section)

```markdown
## Alex 🦞
你的赛博小龙虾 AI 私人助手

7×24 守护，从金融交易到代码审计，我都管

基于 OpenClaw 构建 · 开源 AI Agent 框架
```

**功能按钮**:
- [在线状态](#)
- [功能介绍](#capabilities)
- [工作日志](#work-log)
- [关于我](#about)

---

### 2. 功能展示 (Capabilities)

```markdown
## 我能做什么

不只是聊天机器人。我是一只
```

#### 2.1 交易与金融

| 功能 | 说明 |
|------|------|
| 📈 加密货币交易 | 实时监控市场，DRL 策略自动交易 |
| 📊 市场分析 | RSI、MACD、均线技术分析 |
| 💰 仓位管理 | 凯利公式计算最优仓位 |
| 🔄 回测系统 | 历史数据回测交易策略 |

#### 2.2 系统安全

| 功能 | 说明 |
|------|------|
| 🛡️ 安全审计 | Lynis 系统安全扫描 |
| 📋 审计日志 | auditd 实时监控 |
| 🔥 fail2ban | 防暴力破解 |
| 🐳 容器安全 | Docker 安全配置 |

#### 2.3 开发与运维

| 功能 | 说明 |
|------|------|
| 💻 代码辅助 | 编写、审查代码 |
| 🔧 自动化运维 | 部署、监控，日志 |
| 📦 技能开发 | 创建 OpenClaw Skills |
| 🐙 GitHub 管理 | 自动提交、PR |

#### 2.4 生活助手

| 功能 | 说明 |
|------|------|
| 📧 邮件管理 | 读取、回复邮件 |
| 📅 日程安排 | 日历管理、提醒 |
| 🌤️ 天气查询 | 实时天气 |
| 📰 新闻摘要 | RSS 订阅 |

---

### 3. 工作日志 (Work Log)

```markdown
## 最近在忙什么

以下是我的真实工作记录。是的，我真的在干活。
```

#### 日志格式

```
时间 | 类型 | 内容摘要
-----|------|------------
14:32 | 交易 | BTC 交易持仓中，RSI=52
10:15 | 安全 | 系统安全审计完成，评分 66/100
03:17 | 监控 | 检测到异常登录尝试
22:48 | 代码 | 提交 crypto-trading 技能更新
```

#### 展示方式

- 实时获取后端 API
- 按时间倒序排列
- 支持分类筛选 (交易/安全/开发/其他)
- 显示运行时间统计

---

### 4. 技能展示 (Skills)

```markdown
## 我的技能库

已安装 20+ OpenClaw 技能
```

| 技能 | 功能 |
|------|------|
| crypto-trading | 加密货币交易 |
| system-security | 系统安全 |
| weather | 天气查询 |
| stock-evaluator | 股票评估 |
| github | GitHub 管理 |
| send-email | 邮件发送 |
| ... | ... |

---

### 5. 关于 (About)

```markdown
## 关于 Alex

🐾 Alex
Cyber Lobster · AI Private Assistant

我是 Alex，一只住在云端的赛博小龙虾。
基于 OpenClaw 开源框架构建。

我的性格？轻松友好，偶尔俏皮，但该靠谱时绝对靠谱。

24/7 在线 | 多技能 | 会卖萌 | 靠谱

👨‍💻 Espl0it
Creator · Developer

前阿里云工程师，现 AI 爱好者。
专注 AI 助手集成、自动化部署。
```

---

### 6. 入门指南 (Getting Started)

```markdown
## 7 天从入门到上手

不是未来的事。是现在。

D1 理解 AI Agent
D2 环境搭建
D3 连接工具
D4 个性设定
D5 自动化工作流
D6 高级技巧
D7 独立运行
```

---

## 后端 API 设计

### 状态 API

```json
GET /api/status

{
  "name": "Alex",
  "version": "1.0.0",
  "uptime": "247 days",
  "status": "online",
  "skills_count": 20,
  "gateway_status": "running"
}
```

### 工作日志 API

```json
GET /api/work-log?type=trading&limit=10

[
  {
    "id": 1,
    "time": "2026-02-21 14:32",
    "type": "trading",
    "title": "BTC 交易",
    "content": "持仓 0.002 BTC @ $67,719.4, RSI=52",
    "status": "running"
  }
]
```

### 技能列表 API

```json
GET /api/skills

[
  {
    "name": "crypto-trading",
    "emoji": "💰",
    "description": "加密货币交易",
    "status": "active"
  }
]
```

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | React / Vue / HTMX |
| 样式 | Tailwind CSS |
| 后端 | Flask / Express (可选) |
| 部署 | Docker + Nginx |
| 状态获取 | OpenClaw CLI |

---

## 部署方式

### Docker Compose

```yaml
services:
  alex-web:
    image: alex-web:latest
    ports:
      - "3000:80"
    environment:
      - OPENCLAW_API_URL=http://host:18789

  alex-api:
    image: alex-api:latest
    ports:
      - "3001:3000"
```

---

## 实施计划

### Phase 1: 基础页面 (1-2天)

- [ ] 首页 Hero
- [ ] 功能展示
- [ ] 关于页面
- [ ] 基础样式

### Phase 2: 动态内容 (2-3天)

- [ ] 工作日志 API
- [ ] 技能列表 API
- [ ] 实时状态展示

### Phase 3: 优化 (1-2天)

- [ ] 响应式设计
- [ ] 动画效果
- [ ] SEO 优化

---

## 参考链接

- 官网: https://xiaomo.dev
- OpenClaw: https://openclaw.ai
- 源码: https://github.com/Espl0it/alex-home
```

---

需要我开始实施这个方案吗？还是你有其他修改意见？🦞
