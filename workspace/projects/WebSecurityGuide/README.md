# WebSecurityGuide
Web 安全攻防渗透测试实战指南

## 项目简介

本项目提供 Web 安全渗透测试的实战指南，包含环境搭建、漏洞原理、攻击与防御策略。

## 目录结构

```
WebSecurityGuide/
├── docs/                   # 文档教程
│   ├── chapter1-环境搭建.md
│   ├── chapter2-SQL注入.md
│   ├── chapter3-信息收集.md
│   ├── chapter4-XSS.md
│   ├── chapter5-CSRF.md
│   ├── chapter6-文件上传.md
│   └── chapter7-密码攻击.md
├── tools/                  # 工具集
├── practice/              # 靶场练习
└── README.md
```

## 章节目录

### Chapter 1: 环境搭建
- VMWare 虚拟化平台
- Kali Linux 渗透测试系统
- Docker 环境搭建
- 漏洞靶场搭建 (Metasploitable2, DVWA, SQLI-LABS, Upload-Labs)

### Chapter 2: SQL 注入
- SQLMap 工具使用
- 注入类型与实战演练
- SQL 注入防御

### Chapter 3: 信息收集
- 被动侦察 (Whois, Sublist3r)
- 网络空间测绘 (Shodan, FOFA)
- CMS 指纹识别 (WhatWeb)

### Chapter 4: XSS 跨站脚本攻击
- 反射型 XSS
- 存储型 XSS
- DOM 型 XSS
- XSS 防御策略

### Chapter 5: CSRF 跨站请求伪造
- CSRF 原理
- 攻击与利用
- Token 验证与防御

### Chapter 6: 文件上传漏洞
- 绕过技术
- WebShell
- 文件上传防御

### Chapter 7: 密码攻击
- 暴力破解
- 字典攻击
- 密码破解工具 (Hydra, John, Hashcat)
- 密码安全策略

### Chapter 8: WAF 绕过技术
- WAF 识别
- SQL 注入绕过 (编码、注释、Tamper 脚本)
- XSS 绕过
- 绕过工具 (SQLMap, XSStrike, dalfox)
- WAF 防御策略

## 快速开始

详见各章节文档。

## 靶场端口汇总

| 靶场 | 端口 |
|------|------|
| DVWA | 8080 |
| SQLI-LABS | 8081 |
| Upload-Labs | 8082 |
| Metasploitable2 | 随机 |

## 常用工具

| 工具 | 用途 |
|------|------|
| SQLMap | SQL 注入 |
| Nmap | 端口扫描 |
| Burp Suite | Web 渗透测试 |
| Metasploit | 漏洞利用 |
| Hydra | 密码破解 |

## 免责声明

本项目仅供学习 Web 安全使用，请勿用于非法用途。
