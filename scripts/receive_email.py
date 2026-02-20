#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件接收脚本 - 每15分钟检查新邮件
处理 126 邮箱的特殊限制
"""

import imaplib
import email
import re

# 配置
IMAP_SERVER = "imap.126.com"
EMAIL = "Espl0it@126.com"
PASSWORD = "FST9HYmZGcQfvYXc"
MAX_EMAILS = 5

def get_unread_count():
    """获取未读邮件数量"""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        
        # 使用 STATUS 命令
        status, data = mail.status('INBOX', '(UNSEEN)')
        if status == 'OK':
            match = re.search(r'UNSEEN (\d+)', data[0].decode())
            count = int(match.group(1)) if match else 0
            mail.logout()
            return count, None
        
        mail.logout()
        return 0, None
    except Exception as e:
        return -1, str(e)

def main():
    print(f"📧 检查新邮件...")
    count, error = get_unread_count()
    
    if count > 0:
        print(f"📬 有 {count} 封未读邮件!")
        # 返回结果供 cron 发送通知
        print(f"RESULT: {count} unread emails")
        return f"📬 你有 {count} 封未读邮件！"
    elif count == 0:
        print("📭 没有新邮件")
        return None
    else:
        print(f"⚠️ 无法连接邮箱: {error}")
        return None

if __name__ == "__main__":
    main()
