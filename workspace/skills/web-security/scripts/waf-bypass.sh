#!/bin/bash
# WAF 绕过工具脚本

WAFWAF_VERSION="1.0.0"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# WAF 识别
waf_identify() {
    local target="$1"
    echo -e "${GREEN}[*] 识别 WAF...${NC}"
    
    if command -v whatwaf &> /dev/null; then
        whatwaf --esp -u "$target"
    elif command -v wafw00f &> /dev/null; then
        wafw00f "$target"
    else
        echo -e "${RED}[!] 请安装 whatwaf 或 wafw00f${NC}"
        echo "pip install whatwaf wafw00f"
    fi
}

# SQL 注入绕过
sql_bypass() {
    local url="$1"
    local tamper="${2:-space2comment,between,randomcase}"
    
    echo -e "${GREEN}[*] SQL 注入绕过测试...${NC}"
    echo -e "${YELLOW}[*] URL: $url${NC}"
    echo -e "${YELLOW}[*] Tamper: $tamper${NC}"
    
    sqlmap -u "$url" --batch --tamper="$tamper" --level=5 --risk=3
}

# XSS 绕过
xss_bypass() {
    local url="$1"
    
    echo -e "${GREEN}[*] XSS 绕过测试...${NC}"
    echo -e "${YELLOW}[*] URL: $url${NC}"
    
    if command -v xsstrike &> /dev/null; then
        xsstrike -u "$url" --encode --blind
    elif command -v dalfox &> /dev/null; then
        dalfox url "$url" --blind
    else
        echo -e "${RED}[!] 请安装 xsstrike 或 dalfox${NC}"
    fi
}

# HTTP 代理绕过
proxy_bypass() {
    local url="$1"
    local proxy="${2:-http://127.0.0.1:8080}"
    
    echo -e "${GREEN}[*] 使用代理绕过...${NC}"
    echo -e "${YELLOW}[*] URL: $url${NC}"
    echo -e "${YELLOW}[*] Proxy: $proxy${NC}"
    
    sqlmap -u "$url" --proxy="$proxy" --random-agent --delay=1
}

# 显示帮助
show_help() {
    cat << EOF
Web Security - WAF 绕过工具 v${WAFWAF_VERSION}

用法: websec-waf <command> [options]

命令:
  identify <target>      识别 WAF 类型
  sql <url> [tamper]     SQL 注入绕过
  xss <url>              XSS 绕过测试
  proxy <url> [proxy]    使用代理绕过

示例:
  websec-waf identify http://target.com
  websec-waf sql "http://target.com?id=1"
  websec-waf sql "http://target.com?id=1" "space2comment,between"
  websec-waf xss "http://target.com/search?q=test"
  websec-waf proxy "http://target.com?id=1"

Tamper 脚本组合:
  space2comment,between,randomcase
  space2comment,charencode
  between,equaltolike
EOF
}

# 主命令处理
case "$1" in
    identify)
        waf_identify "$2"
        ;;
    sql)
        sql_bypass "$2" "$3"
        ;;
    xss)
        xss_bypass "$2"
        ;;
    proxy)
        proxy_bypass "$2" "$3"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        show_help
        ;;
esac
