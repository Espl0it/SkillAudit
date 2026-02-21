#!/usr/bin/env python3
"""
Alex Status API - 提供动态内容 API
"""
import json
import subprocess
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# CORS 头
def cors_headers():
    return {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

def get_openclaw_status():
    """获取 OpenClaw 状态"""
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', 'openclaw-gateway'],
            capture_output=True,
            text=True,
            timeout=5
        )
        status = 'running' if result.stdout.strip() == 'active' else 'stopped'
    except:
        status = 'unknown'
    
    return {
        'name': 'Alex',
        'version': '1.0.0',
        'status': status,
        'skills_count': 20,
        'framework': 'OpenClaw'
    }

def get_work_logs():
    """获取工作日志"""
    return [
        {
            'id': 1,
            'time': '2026-02-21 14:32',
            'type': 'trading',
            'title': '交易监控',
            'content': '监控 Top 3 交易标的 (XRP, DOGE, DOT)，当前无 RSI < 35 买入机会'
        },
        {
            'id': 2,
            'time': '2026-02-21 10:15',
            'type': 'security',
            'title': '安全审计',
            'content': '系统安全审计完成，Lynis 评分 66/100'
        },
        {
            'id': 3,
            'time': '2026-02-21 03:17',
            'type': 'backtest',
            'title': '策略回测',
            'content': '完成 SOL DRL 策略回测，收益 +4.94%，优于买入持有 -40.39%'
        },
        {
            'id': 4,
            'time': '2026-02-20 16:32',
            'type': 'coding',
            'title': '代码开发',
            'content': '提交 crypto-trading 技能更新，添加多标的监控功能'
        },
        {
            'id': 5,
            'time': '2026-02-20 14:00',
            'type': 'trading',
            'title': '买入 SOL',
            'content': 'RSI=39.3 买入 SOL 1.18 @ $84.47'
        }
    ]

def get_skills():
    """获取技能列表"""
    return [
        {'name': 'crypto-trading', 'emoji': '💰', 'description': '加密货币交易'},
        {'name': 'system-security', 'emoji': '🛡️', 'description': '系统安全'},
        {'name': 'weather', 'emoji': '🌤️', 'description': '天气查询'},
        {'name': 'stock-evaluator', 'emoji': '📈', 'description': '股票评估'},
        {'name': 'github', 'emoji': '🐙', 'description': 'GitHub 管理'},
        {'name': 'send-email', 'emoji': '📧', 'description': '邮件发送'},
        {'name': 'tavily', 'emoji': '🔍', 'description': 'AI 搜索'},
        {'name': 'summarize', 'emoji': '📝', 'description': 'URL 摘要'},
        {'name': 'gog', 'emoji': '🌐', 'description': 'Google Workspace'},
        {'name': 'wacli', 'emoji': '💬', 'description': 'WhatsApp'},
        {'name': 'proactive-agent', 'emoji': '🧠', 'description': '主动规划'},
        {'name': 'blogwatcher', 'emoji': '📰', 'description': 'RSS 监控'},
        {'name': 'cos-mount', 'emoji': '🐳', 'description': 'COS 挂载'},
        {'name': 'notion', 'emoji': '🎯', 'description': 'Notion 集成'},
        {'name': 'tushare', 'emoji': '🧮', 'description': '金融数据'},
        {'name': 'option-trading', 'emoji': '📊', 'description': '期权交易'},
    ]

def handler(event, context):
    """处理请求"""
    path = event.get('path', '/')
    method = event.get('httpMethod', 'GET')
    
    # CORS 预检
    if method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers(),
            'body': ''
        }
    
    # 路由
    if path == '/api/status':
        return {
            'statusCode': 200,
            'headers': {**cors_headers(), 'Content-Type': 'application/json'},
            'body': json.dumps(get_openclaw_status(), ensure_ascii=False)
        }
    elif path == '/api/work-log':
        return {
            'statusCode': 200,
            'headers': {**cors_headers(), 'Content-Type': 'application/json'},
            'body': json.dumps(get_work_logs(), ensure_ascii=False)
        }
    elif path == '/api/skills':
        return {
            'statusCode': 200,
            'headers': {**cors_headers(), 'Content-Type': 'application/json'},
            'body': json.dumps(get_skills(), ensure_ascii=False)
        }
    else:
        return {
            'statusCode': 404,
            'headers': cors_headers(),
            'body': 'Not Found'
        }

# 本地开发服务器
if __name__ == '__main__':
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import socketserver
    
    PORT = 3001
    
    class Handler(BaseHTTPRequestHandler):
        def do_OPTIONS(self):
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
        
        def do_GET(self):
            event = {'path': self.path, 'httpMethod': 'GET'}
            response = handler(event, None)
            
            self.send_response(response['statusCode'])
            for k, v in response['headers'].items():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(response['body'].encode())
        
        def log_message(self, format, *args):
            print(f"[{self.log_date_time_string()}] {format % args}")
    
    print(f"🚀 Alex API Server 运行在 http://localhost:{PORT}")
    print(f"   - GET /api/status")
    print(f"   - GET /api/work-log")
    print(f"   - GET /api/skills")
    
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    server.serve_forever()
