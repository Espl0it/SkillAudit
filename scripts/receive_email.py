#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件接收脚本 - 每15分钟检查新邮件
有邮件时发送通知，否则静默
"""

import socket
import ssl
import email
import re

IMAP_SERVER = "imap.126.com"
EMAIL = "Espl0it@126.com"
PASSWORD = "FST9HYmZGcQfvYXc"

def get_unread_emails():
    try:
        context = ssl.create_default_context()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = context.wrap_socket(sock, server_hostname=IMAP_SERVER)
        sock.connect((IMAP_SERVER, 993))
        sock.recv(1024)
        
        sock.send(b'A001 ID ()\r\n')
        sock.recv(1024)
        
        sock.send(b'A002 LOGIN Espl0it@126.com FST9HYmZGcQfvYXc\r\n')
        resp = sock.recv(1024)
        if b'OK' not in resp:
            sock.close()
            return []
        
        sock.send(b'A003 SELECT INBOX\r\n')
        resp = sock.recv(4096)
        if b'OK' not in resp:
            sock.close()
            return []
        
        match = re.search(rb'(\d+) UNSEEN', resp)
        unread_count = int(match.group(1)) if match else 0
        
        if unread_count == 0:
            sock.close()
            return []
        
        sock.send(b'A004 SEARCH UNSEEN\r\n')
        resp = sock.recv(4096)
        
        ids = re.findall(rb'\d+', resp.split(b'\r\n')[-2])
        ids = [int(i) for i in ids[-3:]]
        
        emails = []
        for eid in ids:
            sock.send(f'A005 FETCH {eid} (RFC822)\r\n'.encode())
            resp = sock.recv(8192)
            try:
                msg = email.message_from_bytes(resp)
                emails.append({
                    'from': msg['from'],
                    'subject': msg['subject'] or '(无主题)',
                })
            except:
                pass
        
        sock.close()
        return emails
        
    except Exception as e:
        return []

if __name__ == "__main__":
    emails = get_unread_emails()
    if emails:
        print(f"📬 有 {len(emails)} 封新邮件!")
        for mail in emails:
            print(f"来自: {mail['from']}")
            print(f"主题: {mail['subject']}")
    else:
        # Silent exit - no notification
        import sys
        sys.exit(1)  # Exit with error so cron won't announce
