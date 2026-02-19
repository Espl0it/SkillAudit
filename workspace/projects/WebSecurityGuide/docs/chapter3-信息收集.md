# Chapter 3: 信息收集

黑客攻击前通常进行侦察，分为主动侦察和被动侦察。

## 3.1 被动侦察

### 3.1.1 侦察域名

#### Whois 查询

查询域名或 IP 地址的注册信息。

```bash
whois example.com
whois -v -a example.com
whois -i 192.0.2.1
```

**常用 whois 服务器：**
- `whois.internic.net` - 全球域名
- `whois.ripe.net` - 欧洲
- `whois.apnic.net` - 亚洲

#### Sublist3r 子域名扫描

快速发现目标域名的子域名。

**安装：**
```bash
pip install sublist3r
```

**用法：**
```bash
# 基本扫描
sublist3r -d example.com

# 多线程扫描
sublist3r -d example.com -t 10

# 使用搜索引擎
sublist3r -d example.com -e google,yahoo

# 保存结果
sublist3r -d example.com -o output.txt
```

#### Amass - 子域名枚举

更强大的子域名发现工具。

**安装：**
```bash
go install github.com/owasp/amass/v3/...@latest
```

**用法：**
```bash
# 被动扫描
amass enum -passive -d example.com

# 主动扫描
amass enum -active -d example.com

# 暴力破解
amass enum -brute -d example.com
```

### 3.1.2 网络空间测绘

#### Shodan 搜索引擎

搜索互联网上暴露的设备和服务。

**安装与初始化：**
```bash
pip install shodan
shodan init <your_api_key>
```

**常用命令：**
```bash
# 查看公网 IP
shodan myip

# 搜索设备
shodan search Apache
shodan search "Apache/2.4.41"
shodan search "nginx" --facets country

# 搜索特定端口
shodan search "port:22" --facets country
shodan search "port:3306" --facets country
shodan search "port:3389" --facels country

# 查看主机信息
shodan host 192.168.1.1

# 创建警报
shodan alert create my-alert 188.165.1.1

# 列出警报
shodan alert list

# 下载数据
shodan download --limit 100 Redis-data "Redis port:6379"
```

#### FOFA 网络空间资产搜索引擎

国内网络空间资产测绘工具。

**注册：** 建议注册以获得无限搜索次数

**查询语法：**
```bash
# 标题查询
title="index of"
title="后台管理"

# 内容查询
body="login"
body="password"

# 组合查询
title="admin" && body="login"

# IP 范围
ip="192.168.1.0/24"

# 端口查询
port="22"
port="3389"

# 协议查询
protocol="ssh"
protocol="rdp"

# favicon 查询
icon_hash="123456789"

# 正则查询
body=/.{30}/
```

#### ZoomEye 钟馗之眼

国内网络空间搜索引擎。

```bash
# 搜索 Apache
app:"Apache"

# 搜索 SSH
service:"ssh"

# 搜索摄像头
device:"webcam"
```

### 3.1.3 CMS 指纹识别

#### WhatWeb

识别 Web 技术指纹，支持 150+ 种 CMS。

**安装：**
```bash
# Kali 已预装
sudo apt install whatweb
```

**用法：**
```bash
# 基本扫描
whatweb https://example.com

# 详细扫描
whatweb -a 3 https://example.com

# 批量扫描
whatweb -input-file urls.txt

# 输出到文件
whatweb --log-xml results.xml https://example.com
whatweb --log-json results.json https://example.com
whatweb --logCSV results.csv https://example.com
```

#### Wappalyzer

浏览器插件，实时识别网站技术。

#### CMSeek

CMS 扫描工具。

```bash
# 安装
git clone https://github.com/Tuhinshubhra/CMSeeK

# 使用
python3 cmseek.py -u https://example.com
```

### 3.1.4 OSINT 工具

#### theHarvester

收集邮箱、子域名、IP 地址。

**安装：**
```bash
# Kali 已预装
```

**用法：**
```bash
# 基本用法
theHarvester -d example.com -b all

# 使用 Google
theHarvester -d example.com -b google

# 使用 Bing
theHarvester -d example.com -b bing

# 限制结果数
theHarvester -d example.com -b all -l 100
```

#### Recon-ng

全功能 Web  reconnaissance 框架。

**安装：**
```bash
# Kali 已预装
recon-ng
```

**使用：**
```bash
# 启动
recon-ng

# 添加工作区
workspaces create pentest

# 使用模块
modules search
modules load recon/domains-domains/brute_hosts

# 设置域名
set SOURCE example.com

# 运行
run

# 显示结果
show hosts
```

#### Maltego

可视化信息收集工具。

**功能：**
- 域名发现
- 邮箱收集
- 人物调查
- 社交媒体分析
- 可视化关联

### 3.1.5 Google Hacking

使用 Google 搜索语法收集信息。

```bash
# 敏感文件
site:example.com filetype:pdf
site:example.com filetype:doc | filetype:xls

# 目录遍历
site:example.com "index of"

# 登录页面
site:example.com login
site:example.com admin

# 配置文件
site:example.com ext:conf
site:example.com ext:config

# 数据库文件
site:example.com ext:sql
site:example.com ext:db

# 备份文件
site:example.com ext:bak
site:example.com ext:old

# 敏感信息
inurl:password
inurl:admin
intext:password
```

## 3.2 主动侦察

### 3.2.1 端口扫描

#### Nmap 详解

**常用命令：**

```bash
# 基本扫描
nmap 192.168.1.1

# 扫描多个 IP
nmap 192.168.1.1 192.168.1.2

# 扫描网段
nmap 192.168.1.0/24

# 指定端口
nmap -p 80,443 192.168.1.1
nmap -p 1-1000 192.168.1.1

# 扫描所有端口
nmap -p- 192.168.1.1

# 服务版本检测
nmap -sV 192.168.1.1

# 操作系统检测
nmap -O 192.168.1.1

# 全面扫描
nmap -A 192.168.1.1

# SYN 扫描（需要 root）
nmap -sS 192.168.1.1

# TCP 连接扫描
nmap -sT 192.168.1.1

# UDP 扫描
nmap -sU 192.168.1.1

# 输出结果
nmap -oN output.txt 192.168.1.1
nmap -oX output.xml 192.168.1.1
nmap -oA output 192.168.1.1
```

**Nmap 脚本：**

```bash
# 漏洞扫描
nmap --script vuln 192.168.1.1

# 暴力破解
nmap --script brute 192.168.1.1

# SQL 注入检测
nmap --script sql-injection 192.168.1.1

# XSS 检测
nmap --script http-xssed 192.168.1.1

# 弱口令检测
nmap --script default or brute 192.168.1.1
```

### 3.2.2 目录扫描

#### Dirb

```bash
# 基本扫描
dirb http://example.com/

# 使用字典
dirb http://example.com/ /usr/share/dirb/wordlists/big.txt

# 指定扩展名
dirb http://example.com/ -o output.txt
```

#### Gobuster

```bash
# 目录扫描
gobuster dir -u http://example.com -w /usr/share/wordlists/dirb/big.txt

# 子域名扫描
gobuster dns -d example.com -w /usr/share/wordlists/subdomains.txt

# 模糊扩展名
gobuster dir -u http://example.com -x .php,.html,.txt
```

#### FFUF

```bash
# 快速目录扫描
ffuf -u http://example.com/FUZZ -w /usr/share/wordlists/dirb/big.txt

# 子域名扫描
ffuf -u http://example.com -H "Host: FUZZ.example.com" -w subdomains.txt

# 参数 fuzzing
ffuf -u http://example.com/index.php?FUZZ=test -w params.txt
```

### 3.2.3 指纹识别

#### WPScan

WordPress 漏洞扫描。

```bash
# 扫描 WordPress
wpscan --url https://example.com

# 用户枚举
wpscan --url https://example.com --enumerate u

# 漏洞扫描
wpscan --url https://example.com --enumerate vp
```

## 3.3 信息收集防御

1. **域名隐私保护** - 启用域名隐私服务
2. **敏感信息脱敏** - 页面不暴露版本信息
3. **隐藏指纹** - 修改默认 Banner
4. **访问控制** - 限制敏感接口暴露
5. **定期扫描** - 自行检查信息泄露
6. **robots.txt** - 防止敏感目录被爬取
7. **CDN** - 隐藏真实 IP
