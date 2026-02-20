#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件接收脚本 - 每15分钟检查新邮件
使用 socket 直接发送 ID 命令解决 126 邮箱限制
"""

import socket
import ssl
import email
import re
import os
import json
from datetime import datetime

# 配置
IMAP_SERVER = "imap.126.com"
EMAIL = "Espl0it@126.com"
PASSWORD = "FST9HYmZGcQfvYXc"

def send_raw(sock, cmd):
    """发送原始 IMAP 命令"""
    sock.send(cmd.encode())
    responses = []
    while True:
        data = sock.recv(4096)
        responses.append(data)
        if b'\r\n' in data:
            break
    return b''.join(responses)

def get_unread_emails():
    """获取未读邮件"""
    try:
        context = ssl.create_default_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = context.wrap_socket(sock, server_hostname=IMAP_SERVER)
        sock.connect((IMAP_SERVER, 993))
        
        # Read greeting
        sock.recv(1024)
        
        # Send ID first - CRITICAL for 126/163 mail
        sock.send(b'A001 ID ()\r\n')
        sock.recv(1024)
        
        # Login
        sock.send(b'A002 LOGIN Espl0it@126.com FST9HYmZGcQfvYXc\r\n')
        resp = sock.recv(1024)
        if b'OK' not in resp:
            sock.close()
            return [], "Login failed"
        
        # Select INBOX
        sock.send(b'A003 SELECT INBOX\r\n')
        resp = sock.recv(4096)
        if b'OK' not in resp:
            sock.close()
            return [], "Select failed"
        
        # Get unread count
        match = re.search(rb'(\d+) UNSEEN', resp)
        unread_count = int(match.group(1)) if match else 0
        
        if unread_count == 0:
            sock.close()
            return [], None
        
        # Search for unseen emails
        sock.send(b'A004 SEARCH UNSEEN\r\n')
        resp = sock.recv(4096)
        
        # Extract email IDs
        ids = re.findall(rb'\d+', resp.split(b'\r\n')[-2])
        ids = [int(i) for i in ids[-5:]]  # Last 5 unread
        
        emails = []
        for eid in ids:
            # Fetch email
            sock.send(f'A005 FETCH {eid} (RFC822)\r\n'.encode())
            resp = sock.recv(8192)
            
            # Parse email
            try:
                msg = email.message_from_bytes(resp)
                emails.append({
                    'from': msg['from'],
                    'subject': msg['subject'] or '(无主题)',
                    'date': msg['date'],
                })
            except:
                pass
        
        sock.close()
        return emails, None
        
    except Exception as e:
        return [], str(e)

def main():
    print(f"📧 [{datetime.now().strftime('%H:%M:%S')}] 检查新邮件...")
    emails, error = get_unread_emails()
    
    if error:
        print(f"❌ 错误: {error}")
        return
    
    if emails:
        print(f"📬 发现 {len(emails)} 封未读邮件:")
        for i, mail in enumerate(emails, 1):
            print(f"\n--- 邮件 {i} ---")
            print(f"来自: {mail['from']}")
            print(f"主题: {mail['subject']}")
    else:
        print("📭 没有新邮件")

if __name__ == "__main__":
    main()
