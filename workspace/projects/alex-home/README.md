# Alex 🦞 - AI Personal Assistant Homepage

> 你的赛博小龙虾 AI 私人助手主页，基于 [xiaomo.dev](https://xiaomo.dev) 设计理念

![Preview](https://img.shields.io/badge/Alex-Online-brightgreen)
![OpenClaw](https://img.shields.io/badge/Powered-By-OpenClaw-orange)

## 功能特色

- 🟢 实时在线状态
- 📈 加密货币交易监控
- 🛡️ 系统安全审计
- 💻 开发运维自动化
- 📊 金融数据分析
- 📧 邮件智能管理
- 🌤️ 天气实时查询

## 快速开始

### 本地预览

```bash
# 简单方式：直接打开 HTML
open index.html

# 或使用 Python HTTP 服务器
cd alex-home
python3 -m http.server 3000
# 访问 http://localhost:3000
```

### Docker 部署

```bash
# 启动服务
docker-compose up -d

# 访问
# 前端: http://localhost:3000
# API:  http://localhost:3001
```

### API 端点

| 端点 | 说明 |
|------|------|
| `GET /api/status` | 获取状态 |
| `GET /api/work-log` | 工作日志 |
| `GET /api/skills` | 技能列表 |

## 项目结构

```
alex-home/
├── index.html          # 主页面
├── api/
│   └── server.py       # API 服务
├── docker-compose.yml  # Docker 部署
├── README.md
└── PLANNING.md        # 规划方案
```

## 技术栈

- **前端**: HTML5, CSS3, Vanilla JavaScript
- **后端**: Python Flask (可选)
- **部署**: Docker, Nginx

## 部署到云端

### Vercel (免费)

```bash
# 安装 Vercel CLI
npm i -g vercel

# 部署
vercel --prod
```

### Cloudflare Pages (免费)

1. Fork 本项目
2. 连接 Cloudflare Pages
3. 构建命令留空
4. 输出目录填 `/`

## 参考

- [xiaomo.dev](https://xiaomo.dev) - 设计参考
- [OpenClaw](https://openclaw.ai) - AI Agent 框架
- [OpenClaw Docs](https://docs.openclaw.ai) - 官方文档

---

🦞 Built with ❤️ by Espl0it
