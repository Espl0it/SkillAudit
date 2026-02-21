#!/bin/bash
# COS 挂载工具 - Bash 版本
# 使用方法: bash cos_mount.sh <command>

set -e

# 颜色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 配置（使用环境变量或默认值）
COS_SECRET_ID="${COS_SECRET_ID}"
COS_SECRET_KEY="${COS_SECRET_KEY}"
COS_BUCKET="${COS_BUCKET}"
COS_REGION="${COS_REGION:-ap-guangzhou}"
COS_MOUNT_POINT="${COS_MOUNT_POINT:-/mnt/cos}"

# 地域对应 URL
declare -A REGION_URLS=(
    ["ap-guangzhou"]="cos.ap-guangzhou.myqcloud.com"
    ["ap-shanghai"]="cos.ap-shanghai.myqcloud.com"
    ["ap-beijing"]="cos.ap-beijing.myqcloud.com"
    ["ap-hongkong"]="cos.ap-hongkong.myqcloud.com"
    ["ap-singapore"]="cos.ap-singapore.myqcloud.com"
)

# 获取 COS URL
get_cos_url() {
    echo "${REGION_URLS[$COS_REGION]:-cos.${COS_REGION}.myqcloud.com}"
}

# 检查依赖
check_deps() {
    echo "检查依赖..."
    
    if ! command -v fusermount &> /dev/null; then
        echo -e "${RED}❌ 错误: fusermount 未安装${NC}"
        echo "   Ubuntu: sudo apt-get install fuse"
        echo "   CentOS: sudo yum install fuse"
        return 1
    fi
    
    if ! command -v cosfs &> /dev/null; then
        echo -e "${RED}❌ 错误: cosfs 未安装${NC}"
        echo "   请运行: bash $0 install"
        return 1
    fi
    
    echo -e "${GREEN}✅ 依赖检查通过${NC}"
    return 0
}

# 配置密钥
config_creds() {
    if [ -z "$COS_SECRET_ID" ] || [ -z "$COS_SECRET_KEY" ]; then
        echo -e "${RED}❌ 请设置环境变量 COS_SECRET_ID 和 COS_SECRET_KEY${NC}"
        return 1
    fi
    
    if [ -z "$COS_BUCKET" ]; then
        echo -e "${RED}❌ 请设置环境变量 COS_BUCKET${NC}"
        return 1
    fi
    
    # 创建密钥文件
    sudo mkdir -p /etc
    echo "${COS_BUCKET}:${COS_SECRET_ID}:${COS_SECRET_KEY}" | sudo tee /etc/passwd-cosfs > /dev/null
    sudo chmod 640 /etc/passwd-cosfs
    
    echo -e "${GREEN}✅ 密钥已配置到 /etc/passwd-cosfs${NC}"
}

# 挂载 COS
mount_cos() {
    # 检查参数
    if [ -z "$COS_BUCKET" ] || [ -z "$COS_MOUNT_POINT" ]; then
        echo -e "${RED}❌ 请设置环境变量 COS_BUCKET 和 COS_MOUNT_POINT${NC}"
        return 1
    fi
    
    # 创建挂载点
    sudo mkdir -p "$COS_MOUNT_POINT"
    
    # 获取 COS URL
    COS_URL=$(get_cos_url)
    
    # 检查是否已挂载
    if mount | grep -q "$COS_MOUNT_POINT"; then
        echo -e "${YELLOW}⚠️ $COS_MOUNT_POINT 已经挂载${NC}"
        return 0
    fi
    
    echo -e "${GREEN}📦 正在挂载 ${COS_BUCKET} 到 ${COS_MOUNT_POINT}...${NC}"
    
    # 挂载
    sudo cosfs "$COS_BUCKET" "$COS_MOUNT_POINT" \
        -ourl="http://${COS_URL}" \
        -odbglevel=info \
        -oallow_other \
        -onoxattr \
        2>&1
    
    if mount | grep -q "$COS_MOUNT_POINT"; then
        echo -e "${GREEN}✅ 挂载成功!${NC}"
    else
        echo -e "${RED}❌ 挂载失败${NC}"
        return 1
    fi
}

# 卸载 COS
umount_cos() {
    if [ -z "$COS_MOUNT_POINT" ]; then
        echo -e "${RED}❌ 请设置环境变量 COS_MOUNT_POINT${NC}"
        return 1
    fi
    
    if ! mount | grep -q "$COS_MOUNT_POINT"; then
        echo -e "${YELLOW}⚠️ $COS_MOUNT_POINT 未挂载${NC}"
        return 0
    fi
    
    echo -e "${GREEN}📦 正在卸载...${NC}"
    sudo fusermount -u "$COS_MOUNT_POINT" 2>/dev/null || \
    sudo fusermount -uz "$COS_MOUNT_POINT" 2>/dev/null || \
    sudo umount -l "$COS_MOUNT_POINT" 2>/dev/null
    
    if mount | grep -q "$COS_MOUNT_POINT"; then
        echo -e "${RED}❌ 卸载失败${NC}"
        return 1
    else
        echo -e "${GREEN}✅ 卸载成功!${NC}"
    fi
}

# 查看状态
status() {
    echo "========================================"
    echo "       COS 挂载状态"
    echo "========================================"
    echo ""
    echo "配置信息:"
    echo "  存储桶: ${COS_BUCKET:-未设置}"
    echo "  地域: ${COS_REGION}"
    echo "  挂载点: ${COS_MOUNT_POINT}"
    echo ""
    
    if mount | grep -q "$COS_MOUNT_POINT"; then
        echo -e "${GREEN}✅ 状态: 已挂载${NC}"
        mount | grep "$COS_MOUNT_POINT"
    else
        echo -e "${RED}❌ 状态: 未挂载${NC}"
    fi
    
    echo ""
    df -h "$COS_MOUNT_POINT" 2>/dev/null || true
}

# 开机自动挂载
enable_auto_mount() {
    if [ -z "$COS_BUCKET" ] || [ -z "$COS_MOUNT_POINT" ]; then
        echo -e "${RED}❌ 请设置环境变量 COS_BUCKET 和 COS_MOUNT_POINT${NC}"
        return 1
    fi
    
    COS_URL=$(get_cos_url)
    
    # 添加到 /etc/fstab
    FSTAB_LINE="cosfs#${COS_BUCKET} ${COS_MOUNT_POINT} fuse _netdev,allow_other,url=http://${COS_URL},multiregion=0 0 0"
    
    if grep -q "$COS_MOUNT_POINT" /etc/fstab 2>/dev/null; then
        echo -e "${YELLOW}⚠️ 自动挂载已配置${NC}"
        return 0
    fi
    
    echo "$FSTAB_LINE" | sudo tee -a /etc/fstab > /dev/null
    echo -e "${GREEN}✅ 已添加开机自动挂载${NC}"
}

# 安装 COSFS
install_cosfs() {
    echo "========================================"
    echo "       安装 COSFS"
    echo "========================================"
    
    # 检测系统
    if [ -f /etc/debian_version ]; then
        echo "检测到 Debian/Ubuntu 系统"
        sudo apt-get update
        sudo apt-get install -y fuse libfuse-dev build-essential wget
    elif [ -f /etc/redhat-release ]; then
        echo "检测到 CentOS/RHEL 系统"
        sudo yum install -y fuse fuse-devel gcc gcc-c++ wget
    else
        echo -e "${RED}❌ 不支持的系统${NC}"
        return 1
    fi
    
    # 下载 COSFS
    TMP_DIR="/tmp/cosfs-install"
    mkdir -p "$TMP_DIR"
    cd "$TMP_DIR"
    
    echo "下载 COSFS..."
    wget -q "https://github.com/tencentyun/cosfs-v1.0.19.tar.gz" -O cosfs.tar.gz 2>/dev/null || \
    wget -q "https://github.com/tencentyun/cosfs/releases/download/v1.0.19/cosfs_1.0.19_amd64.deb" -O cosfs.deb 2>/dev/null
    
    if [ -f cosfs.deb ]; then
        sudo dpkg -i cosfs.deb
    elif [ -f cosfs.tar.gz ]; then
        tar -zxf cosfs.tar.gz
        cd cosfs-*
        ./configure && make && sudo make install
    else
        echo -e "${RED}❌ 下载失败，请手动安装${NC}"
        echo "参考: https://github.com/tencentyun/cosfs"
        return 1
    fi
    
    # 验证
    if command -v cosfs &> /dev/null; then
        echo -e "${GREEN}✅ COSFS 安装成功!${NC}"
    else
        echo -e "${RED}❌ 安装失败${NC}"
        return 1
    fi
}

# 帮助
help() {
    echo "
========================================
       COS 挂载工具
========================================

用法:
  bash $0 <command>

命令:
  mount              挂载 COS
  umount             卸载 COS
  status             查看状态
  install            安装 COSFS
  enable-auto        开机自动挂载
  help               显示帮助

环境变量:
  COS_SECRET_ID       腾讯云 SecretId (必填)
  COS_SECRET_KEY     腾讯云 SecretKey (必填)
  COS_BUCKET         存储桶名称 (必填)
  COS_REGION         地域 (默认: ap-guangzhou)
  COS_MOUNT_POINT    挂载点 (默认: /mnt/cos)

示例:
  # 设置环境变量
  export COS_SECRET_ID=your-secret-id
  export COS_SECRET_KEY=your-secret-key
  export COS_BUCKET=your-bucket-1250000000
  export COS_REGION=ap-guangzhou
  export COS_MOUNT_POINT=/mnt/cos
  
  # 挂载
  bash $0 mount
  
  # 查看状态
  bash $0 status
========================================
"
}

# 主程序
case "${1:-help}" in
    mount)
        check_deps
        config_creds
        mount_cos
        ;;
    umount|unmount)
        umount_cos
        ;;
    status)
        status
        ;;
    install)
        install_cosfs
        ;;
    enable-auto)
        enable_auto_mount
        ;;
    help|--help|-h)
        help
        ;;
    *)
        echo -e "${RED}未知命令: $1${NC}"
        help
        ;;
esac
