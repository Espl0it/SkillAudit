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

# 脚本所在目录（用于查找 .env）
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(SCRIPT_DIR, ".env")


def load_env(path=None):
    """从 .env 文件加载配置到 os.environ（不依赖 python-dotenv）"""
    env_file = path or ENV_PATH
    if not os.path.isfile(env_file):
        return

    with open(env_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"").strip()
                if key:
                    os.environ.setdefault(key, value)


# 先加载 .env，再读取配置（环境变量优先于 .env）
load_env()

# 配置（从 .env / 环境变量读取，无硬编码默认值）
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

    # 挂载命令（新版 cosfs 使用 -o key=value 格式）
    opts = f"url=http://{cos_url},dbglevel=info,allow_other"
    cmd = [
        "cosfs",
        COS_BUCKET,
        COS_MOUNT_POINT,
        "-o",
        opts,
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
    """安装 COSFS（从 GitHub 源码编译 v1.0.24）"""
    system = platform.system()
    cosfs_version = "1.0.24"
    cosfs_url = f"https://github.com/tencentyun/cosfs/archive/refs/tags/v{cosfs_version}.tar.gz"

    work_dir = "/tmp/cosfs-build"
    cosfs_dir = f"{work_dir}/cosfs-{cosfs_version}"

    if system != "Linux":
        print("❌ 仅支持 Linux 系统")
        return False

    print("📦 开始安装 COSFS...")

    # 安装依赖
    if os.path.exists("/etc/debian_version"):
        print("检测到 Ubuntu/Debian 系统")
        deps = [
            "fuse",
            "libfuse-dev",
            "build-essential",
            "automake",
            "autoconf",
            "libtool",
            "pkg-config",
            "libcurl4-openssl-dev",
            "libxml2-dev",
        ]
        subprocess.run(["sudo", "apt-get", "update"], check=False)
        subprocess.run(["sudo", "apt-get", "install", "-y"] + deps, check=False)

    elif os.path.exists("/etc/redhat-release"):
        print("检测到 CentOS/RHEL 系统")
        deps = [
            "fuse",
            "fuse-devel",
            "gcc",
            "gcc-c++",
            "make",
            "automake",
            "autoconf",
            "libtool",
            "pkgconfig",
            "libcurl-devel",
            "libxml2-devel",
        ]
        subprocess.run(["sudo", "yum", "install", "-y"] + deps, check=False)

    else:
        print("⚠️ 未识别的发行版，请手动安装 fuse、libfuse-dev、libcurl、libxml2 及编译工具")

    # 下载源码
    os.makedirs(work_dir, exist_ok=True)
    tarball = f"{work_dir}/cosfs.tar.gz"

    print(f"下载 COSFS v{cosfs_version}...")
    ret = subprocess.run(
        ["wget", "-q", "-O", tarball, cosfs_url],
        cwd=work_dir,
        capture_output=True,
    )
    if ret.returncode != 0 or not os.path.exists(tarball):
        print(f"❌ 下载失败: {cosfs_url}")
        return False

    # 解压（若目录已存在则先删除，避免旧文件干扰）
    if os.path.isdir(cosfs_dir):
        subprocess.run(["rm", "-rf", cosfs_dir], check=False)
    ret = subprocess.run(["tar", "-zxf", "cosfs.tar.gz"], cwd=work_dir, capture_output=True)
    if ret.returncode != 0 or not os.path.isdir(cosfs_dir):
        print("❌ 解压失败")
        return False

    # 生成 configure 并编译安装
    print("编译 COSFS...")
    for step, cmd in [
        ("./autogen.sh", ["./autogen.sh"]),
        ("./configure", ["./configure"]),
        ("make", ["make", "-j" + str(os.cpu_count() or 2)]),
        ("make install", ["sudo", "make", "install"]),
    ]:
        ret = subprocess.run(cmd, cwd=cosfs_dir, capture_output=True, text=True)
        if ret.returncode != 0:
            print(f"❌ {step} 失败: {ret.stderr or ret.stdout}")
            return False

    # 验证
    result = subprocess.run(["which", "cosfs"], capture_output=True)
    if result.returncode == 0:
        print("✅ COSFS 安装成功!")
        return True

    print("❌ COSFS 安装失败（未找到 cosfs 命令）")
    return False


def main():
    if len(sys.argv) < 2:
        print("""
📖 COS 挂载工具

用法:
  python3 cos_mount.py <command>

命令:
  mount              挂载 COS
  umount             卸载 COS
  status             查看状态
  install            安装 COSFS
  enable-auto        开机自动挂载

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
        if not config_credentials():
            sys.exit(1)
        sys.exit(0 if mount_cos() else 1)

    elif cmd == "umount":
        sys.exit(0 if umount_cos() else 1)

    elif cmd == "status":
        sys.exit(0 if status() else 1)

    elif cmd == "install":
        sys.exit(0 if install_cosfs() else 1)

    elif cmd == "enable-auto":
        sys.exit(0 if enable_auto_mount() else 1)

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
