#!/bin/bash
# Web Security 技能脚本

# 端口扫描
websec_nmap() {
    local target="$1"
    nmap -sS -sV -O "$target"
}

# SQL 注入检测
websec_sqlmap() {
    local url="$1"
    sqlmap -u "$url" --batch --dbs
}

# Web 漏洞扫描
websec_nikto() {
    local target="$1"
    nikto -h "$target"
}

# 目录扫描
websec_dirb() {
    local target="$1"
    dirb "$target"
}

# 指纹识别
websec_whatweb() {
    local target="$1"
    whatweb "$target"
}

# XSS 扫描
websec_xss() {
    local url="$1"
    dalfox url "$url"
}

# 主命令处理
case "$1" in
    nmap)
        websec_nmap "${@:2}"
        ;;
    sqlmap)
        websec_sqlmap "${@:2}"
        ;;
    nikto)
        websec_nikto "${@:2}"
        ;;
    dirb)
        websec_dirb "${@:2}"
        ;;
    whatweb)
        websec_whatweb "${@:2}"
        ;;
    xss)
        websec_xss "${@:2}"
        ;;
    help|*)
        echo "Web Security 技能"
        echo ""
        echo "用法: websec <command> [options]"
        echo ""
        echo "命令:"
        echo "  nmap <target>     端口扫描"
        echo "  sqlmap <url>      SQL 注入检测"
        echo "  nikto <target>   Web 漏洞扫描"
        echo "  dirb <target>    目录扫描"
        echo "  whatweb <target> 指纹识别"
        echo "  xss <url>        XSS 扫描"
        ;;
esac
