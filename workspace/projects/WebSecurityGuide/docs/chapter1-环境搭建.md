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

## 1.2 安装 Docker 环境

### Docker 基本用法

| 功能 | 命令 |
|------|------|
| 运行容器 | `docker run -it ubuntu /bin/bash` |
| 列出容器 | `docker ps -a` |
| 停止容器 | `docker stop <container_id>` |
| 删除容器 | `docker rm <container_id>` |
| 创建镜像 | `docker build -t myimage .` |
| 拉取镜像 | `docker pull myimage` |

## 1.3 搭建漏洞环境

### 1.3.1 Metasploitable2

基于 Linux 的渗透测试环境，包含多种常见漏洞。

**下载地址：** https://github.com/rapid7/metasploitable2

### 1.3.2 DVWA (Damn Vulnerable Web Application)

**Docker 搭建：**
```bash
docker run -d -p 8080:80 --name dvwa vulnerables/web-dvwa
# 访问 http://localhost:8080
# 默认用户名/密码: admin/admin
```

### 1.3.3 SQLI-LABS

SQL 注入练习平台。

**Docker 搭建：**
```bash
docker pull acgpiano/sqli-labs
docker run -d -p 8081:80 --name sqli-labs acgpiano/sqli-labs
# 访问 http://localhost:8081
```

### 1.3.4 Upload-Labs

文件上传漏洞练习平台。

**Docker 搭建：**
```bash
docker pull c0ny1/upload-labs
docker run -d -p 8082:80 --name upload-labs c0ny1/upload-labs
# 访问 http://localhost:8082
```

## 靶场端口汇总

| 靶场 | 端口 |
|------|------|
| DVWA | 8080 |
| SQLI-LABS | 8081 |
| Upload-Labs | 8082 |
