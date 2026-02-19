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

# 保存结果
sublist3r -d example.com -o output.txt
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

# 查看主机信息
shodan host 192.168.1.1

# 创建警报
shodan alert create my-alert 188.165.1.1

# 列出警报
shodan alert list
```

#### FOFA 网络空间资产搜索引擎

国内网络空间资产测绘工具。

**注册：** 建议注册以获得无限搜索次数

**查询语法：**
```bash
# 标题查询
title="index of"

# 内容查询
body="login"

# 组合查询
title="admin" && body="login"

# 正则查询
body=/.{30}/
```

### 3.1.3 CMS 指纹识别

#### WhatWeb

识别 Web 技术指纹，支持 150+ 种 CMS。

**安装：**
```bash
# Kali Linux 已预装
# 或通过 apt 安装
sudo apt install whatweb
```

**用法：**
```bash
# 基本扫描
whatweb https://example.com

# 详细扫描
whatweb -a 3 https://example.com

# 输出到文件
whatweb --log-xml results.xml https://example.com
```

**常用参数：**
| 参数 | 说明 |
|------|------|
| `-a` | 探测等级 (1-4) |
| `--log-xml` | XML 格式输出 |
| `--log-json` | JSON 格式输出 |

## 信息收集防御

1. **域名隐私保护** - 启用域名隐私服务
2. **敏感信息脱敏** - 页面不暴露版本信息
3. **隐藏指纹** - 修改默认 Banner
4. **访问控制** - 限制敏感接口暴露
5. **定期扫描** - 自行检查信息泄露
