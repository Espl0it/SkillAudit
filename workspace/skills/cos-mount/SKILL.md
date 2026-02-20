---
name: cos-mount
description: 腾讯云 COS 对象存储挂载工具，支持挂载、卸载、开机自动挂载
metadata:
  openclaw:
    emoji: ☁️
    requires:
      anyBins: ["fusermount", "make", "g++"]
---

# COS Mount Skill

腾讯云 COS (对象存储) 挂载工具，基于 COSFS

## 配置

### 环境变量

| 变量 | 必填 | 说明 |
|------|------|------|
| COS_SECRET_ID | ✅ | 腾讯云 SecretId |
| COS_SECRET_KEY | ✅ | 腾讯云 SecretKey |
| COS_BUCKET | ✅ | 存储桶名称 (如 examplebucket-1250000000) |
| COS_REGION | ✅ | 地域 (如 ap-guangzhou) |
| COS_MOUNT_POINT | ✅ | 本地挂载点 (如 /mnt/cos) |

### 示例配置

```json
{
  "skills": {
    "entries": {
      "cos-mount": {
        "enabled": true,
        "env": {
          "COS_SECRET_ID": "your-secret-id",
          "COS_SECRET_KEY": "your-secret-key",
          "COS_BUCKET": "examplebucket-1250000000",
          "COS_REGION": "ap-guangzhou",
          "COS_MOUNT_POINT": "/mnt/cos"
        }
      }
    }
  }
}
```

## 使用方法

### 1. 安装 COSFS

```bash
# 安装依赖
sudo apt-get update
sudo apt-get install -y fuse libfuse-dev

# 下载并编译安装 COSFS
wget https://github.com/tencentyun/cosfs-v1.0.19.tar.gz
tar -zxf cosfs-v1.0.19.tar.gz
cd cosfs-v1.0.19
./configure
make
sudo make install
```

### 2. 挂载 COS

```bash
# 方式一：使用环境变量
python3 ~/.openclaw/workspace/skills/cos-mount/cos_mount.py mount

# 方式二：命令行参数
python3 ~/.openclaw/workspace/skills/cos-mount/cos_mount.py mount --bucket examplebucket-1250000000 --region ap-guangzhou --point /mnt/cos
```

### 3. 卸载 COS

```bash
python3 ~/.openclaw/workspace/skills/cos-mount/cos_mount.py umount
```

### 4. 开机自动挂载

```bash
python3 ~/.openclaw/workspace/skills/cos_mount.py enable_auto_mount
```

### 5. 查看状态

```bash
python3 ~/.openclaw/workspace/skills/cos_mount.py status
```

## 地域对应表

| 地域 | 节点 URL |
|------|----------|
| ap-guangzhou | cos.ap-guangzhou.myqcloud.com |
| ap-shanghai | cos.ap-shanghai.myqcloud.com |
| ap-beijing | cos.ap-beijing.myqcloud.com |
| ap-hongkong | cos.ap-hongkong.myqcloud.com |
| ap-singapore | cos.ap-singapore.myqcloud.com |

## 故障排查

### 问题：Bucket not exist
- 检查 -ourl 参数，确保 URL 中不携带 Bucket 部分

### 问题：Transport endpoint is not connected
```bash
# 重新挂载
fusermount -uz /mnt/cos
python3 ~/.openclaw/workspace/skills/cos_mount.py mount
```

### 问题：Permission denied
- 确保密钥文件权限为 640

## 注意事项

1. COSFS 适合 POSIX 语义访问，不适合高 IO 场景
2. 大文件上传会占用本地磁盘缓存
3. 建议使用 -oensure_diskfree 参数预留磁盘空间
