#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COS 挂载工具 - OpenClaw Skill
支持挂载、卸载、开机自动挂载
"""

import os
import sys
import subprocess
import platform

# 配置（从环境变量读取）
COS_SECRET_ID = os.getenv("COS_SECRET_ID", "")
COS_SECRET_KEY = os.getenv("COS_SECRET_KEY", "")
COS_BUCKET = os.getenv("COS_BUCKET", "")
COS_REGION = os.getenv("COS_REGION", "ap-guangzhou")
COS_MOUNT_POINT = os.getenv("COS_MOUNT_POINT", "/mnt/cos")

# 地域对应 URL
REGION_URLS = {
    "ap-guangzhou": "cos.ap-guangzhou.myqcloud.com",
    "ap-shanghai": "cos.ap-shanghai.myqcloud.com",
    "ap-beijing": "cos.ap-beijing.myqcloud.com",
    "ap-hongkong": "cos.ap-hongkong.myqcloud.com",
    "ap-singapore": "cos.ap-singapore.myqcloud.com",
}

def get_cos_url(region):
    """获取 COS 节点 URL"""
    return REGION_URLS.get(region, f"cos.{region}.myqcloud.com")

def check_dependencies():
    """检查依赖"""
    # 检查 fuse
    result = subprocess.run(["which", "fusermount"], capture_output=True)
    if result.returncode != 0:
        print("❌ 错误: 请先安装 fuse")
        print("   Ubuntu: sudo apt-get install fuse libfuse-dev")
        print("   CentOS: sudo yum install fuse")
        return False
    
    # 检查 cosfs
    result = subprocess.run(["which", "cosfs"], capture_output=True)
    if result.returncode != 0:
        print("❌ 错误: 请先安装 COSFS")
        print("   参考: https://github.com/tencentyun/cosfs")
        return True  # 继续，可能在其他路径
    
    return True

def config_credentials():
    """配置密钥"""
    if not COS_SECRET_ID or not COS_SECRET_KEY:
        print("❌ 错误: 请设置环境变量 COS_SECRET_ID 和 COS_SECRET_KEY")
        return False
    
    # 创建密钥文件
    os.makedirs("/etc", exist_ok=True)
    cred_file = "/etc/passwd-cosfs"
    
    with open(cred_file, "w") as f:
        f.write(f"{COS_BUCKET}:{COS_SECRET_ID}:{COS_SECRET_KEY}")
    
    os.chmod(cred_file, 0o640)
    print(f"✅ 密钥已配置到 {cred_file}")
    return True

def mount_cos():
    """挂载 COS"""
    if not all([COS_BUCKET, COS_REGION, COS_MOUNT_POINT]):
        print("❌ 错误: 请设置环境变量 COS_BUCKET, COS_REGION, COS_MOUNT_POINT")
        return False
    
    # 创建挂载点
    os.makedirs(COS_MOUNT_POINT, exist_ok=True)
    
    # 获取 URL
    cos_url = get_cos_url(COS_REGION)
    
    # 检查是否已挂载
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    if COS_MOUNT_POINT in result.stdout:
        print(f"⚠️ {COS_MOUNT_POINT} 已经挂载")
        return True
    
    # 挂载命令
    cmd = [
        "cosfs",
        COS_BUCKET,
        COS_MOUNT_POINT,
        "-ourl", f"http://{cos_url}",
        "-odbglevel", "info",
        "-oallow_other",
    ]
    
    print(f"📦 正在挂载 {COS_BUCKET} 到 {COS_MOUNT_POINT}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ 挂载成功!")
        return True
    else:
        print(f"❌ 挂载失败: {result.stderr}")
        return False

def umount_cos():
    """卸载 COS"""
    if not COS_MOUNT_POINT:
        print("❌ 错误: 请设置环境变量 COS_MOUNT_POINT")
        return False
    
    # 检查是否已挂载
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    if COS_MOUNT_POINT not in result.stdout:
        print(f"⚠️ {COS_MOUNT_POINT} 未挂载")
        return True
    
    # 卸载
    print(f"📦 正在卸载 {COS_MOUNT_POINT}...")
    result = subprocess.run(["fusermount", "-u", COS_MOUNT_POINT], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ 卸载成功!")
        return True
    else:
        # 尝试强制卸载
        result = subprocess.run(["fusermount", "-uz", COS_MOUNT_POINT], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 卸载成功 (force)!")
            return True
        print(f"❌ 卸载失败: {result.stderr}")
        return False

def enable_auto_mount():
    """开机自动挂载"""
    if not all([COS_BUCKET, COS_REGION, COS_MOUNT_POINT]):
        print("❌ 错误: 请设置环境变量")
        return False
    
    cos_url = get_cos_url(COS_REGION)
    
    # 添加到 /etc/fstab
    fstab_line = f"cosfs#{COS_BUCKET} {COS_MOUNT_POINT} fuse _netdev,allow_other,url=http://{cos_url},multiregion=0 0 0\n"
    
    # 检查是否已存在
    if os.path.exists("/etc/fstab"):
        with open("/etc/fstab", "r") as f:
            if COS_MOUNT_POINT in f.read():
                print("⚠️ 自动挂载已配置")
                return True
    
    with open("/etc/fstab", "a") as f:
        f.write(fstab_line)
    
    print("✅ 已添加开机自动挂载")
    return True

def status():
    """查看挂载状态"""
    result = subprocess.run(["df", "-h"], capture_output=True, text=True)
    
    print("=== COS 挂载状态 ===\n")
    
    if COS_MOUNT_POINT in result.stdout:
        for line in result.stdout.split("\n"):
            if COS_MOUNT_POINT in line:
                print(f"✅ 已挂载: {line}")
                return True
    
    print(f"❌ 未挂载 (挂载点: {COS_MOUNT_POINT})")
    return False

def install_cosfs():
    """安装 COSFS"""
    system = platform.system()
    
    if system != "Linux":
        print("❌ 仅支持 Linux 系统")
        return False
    
    print("📦 开始安装 COSFS...")
    
    # 检查系统
    if os.path.exists("/etc/debian_version"):
        # Debian/Ubuntu
        print("检测到 Ubuntu/Debian 系统")
        subprocess.run(["sudo", "apt-get", "update"], check=False)
        subprocess.run(["sudo", "apt-get", "install", "-y", "fuse", "libfuse-dev", "build-essential"], check=False)
    elif os.path.exists("/etc/redhat-release"):
        # CentOS/RHEL
        print("检测到 CentOS/RHEL 系统")
        subprocess.run(["sudo", "yum", "install", "-y", "fuse", "fuse-devel", "gcc", "gcc-c++"], check=False)
    
    # 下载并编译 COSFS
    work_dir = "/tmp/cosfs-build"
    os.makedirs(work_dir, exist_ok=True)
    
    print("下载 COSFS...")
    subprocess.run([
        "wget", "-O", f"{work_dir}/cosfs.tar.gz",
        "https://github.com/tencentyun/cosfs-v1.0.19.tar.gz"
    ], cwd=work_dir, check=False)
    
    if not os.path.exists(f"{work_dir}/cosfs.tar.gz"):
        print("❌ 下载失败，请手动安装")
        return False
    
    subprocess.run(["tar", "-zxf", "cosfs.tar.gz"], cwd=work_dir, check=False)
    
    # 编译
    cosfs_dir = f"{work_dir}/cosfs-v1.0.19"
    if os.path.exists(cosfs_dir):
        subprocess.run(["./configure"], cwd=cosfs_dir, check=False)
        subprocess.run(["make"], cwd=cosfs_dir, check=False)
        subprocess.run(["sudo", "make", "install"], cwd=cosfs_dir, check=False)
    
    # 验证
    result = subprocess.run(["which", "cosfs"], capture_output=True)
    if result.returncode == 0:
        print("✅ COSFS 安装成功!")
        return True
    else:
        print("❌ COSFS 安装失败")
        return False

def main():
    if len(sys.argv) < 2:
        print("""
📖 COS 挂载工具

用法:
  python3 cos_mount.py <command>

命令:
  mount              挂载 COS
  umount            卸载 COS
  status            查看状态
  install           安装 COSFS
  enable-auto       开机自动挂载

环境变量:
  COS_SECRET_ID      腾讯云 SecretId
  COS_SECRET_KEY     腾讯云 SecretKey
  COS_BUCKET         存储桶名称
  COS_REGION         地域 (默认: ap-guangzhou)
  COS_MOUNT_POINT    挂载点 (默认: /mnt/cos)
""")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "mount":
        if not check_dependencies():
            sys.exit(1)
        config_credentials()
        mount_cos()
    elif cmd == "umount":
        umount_cos()
    elif cmd == "status":
        status()
    elif cmd == "install":
        install_cosfs()
    elif cmd == "enable-auto":
        enable_auto_mount()
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
