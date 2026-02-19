# Chapter 7: 密码攻击

## 7.1 密码攻击简介

密码攻击是指通过各种手段获取或破解用户密码的攻击方式。

## 7.2 密码攻击类型

### 7.2.1 暴力破解

使用所有可能的字符组合尝试登录。

**工具：Hydra**

```bash
# SSH 暴力破解
hydra -L users.txt -P passwords.txt ssh://192.168.1.100

# HTTP POST 暴力破解
hydra -L users.txt -P passwords.txt 192.168.1.100 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# FTP 暴力破解
hydra -L users.txt -P passwords.txt ftp://192.168.1.100
```

### 7.2.2 字典攻击

使用预定义的密码字典进行尝试。

```bash
# 使用字典
hydra -L users.txt -P common-passwords.txt ssh://192.168.1.100
```

### 7.2.3 社工库攻击

利用泄露的数据库进行攻击。

```bash
# 在社工库中搜索邮箱
grep "user@example.com" leaked_db.txt
```

### 7.2.4 彩虹表攻击

使用预计算的哈希表破解密码。

**工具：RainbowCrack**

```bash
# 生成彩虹表
rtgen md5 ascii 32 7 0 10000 16 0 0

# 破解
rcrack *.rt -h hash
```

## 7.3 密码破解工具

### 7.3.1 John the Ripper

```bash
# 破解shadow文件
unshadow /etc/passwd /etc/shadow > crackme.txt
john crackme.txt

# 使用字典
john --wordlist=passwords.txt crackme.txt

# 查看已破解密码
john --show crackme.txt
```

### 7.3.2 Hashcat

```bash
# MD5 破解
hashcat -m 0 hash.txt passwords.txt

# SHA256 破解
hashcat -m 1400 hash.txt passwords.txt

# WPA/WPA2 破解
hashcat -m 2500 handshake.hccapx wordlist.txt
```

### 7.3.3 常见哈希类型

| 类型 | Hashcat ID |
|------|------------|
| MD5 | 0 |
| SHA1 | 100 |
| SHA256 | 1400 |
| bcrypt | 3200 |
| WPA/WPA2 | 2500 |
| MySQL | 300 |

## 7.4 密码安全

### 7.4.1 密码强度

- 长度至少 12 位
- 包含大小写字母、数字、特殊字符
- 不使用常见密码
- 定期更换密码

### 7.4.2 密码存储

```php
# 使用 password_hash()
$hash = password_hash($password, PASSWORD_BCRYPT);

// 验证
if (password_verify($password, $hash)) {
    // 登录成功
}
```

### 7.4.3 多因素认证 (MFA)

- 短信验证码
- 邮件验证码
- 硬件令牌 (U2F)
- 生物识别

### 7.4.4 账户锁定

```php
$max_attempts = 5;
$lockout_time = 900; // 15分钟

if ($attempts >= $max_attempts) {
    // 锁定账户
}
```

### 7.4.5 密码安全总结

| 安全措施 | 说明 |
|----------|------|
| 强密码策略 | 长度+复杂度 |
| 密码哈希 | 使用 bcrypt/scrypt |
| 账户锁定 | 防止暴力破解 |
| 多因素认证 | 二次验证 |
| 定期更换 | 降低风险 |
