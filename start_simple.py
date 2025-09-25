#!/usr/bin/env python
"""
简单的Django聊天服务器启动脚本
"""
import os
import sys

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

print("🚀 启动Django聊天服务器...")
print("📡 支持HTTP API和WebSocket连接")
print("🌐 服务器地址: http://localhost:8000")
print("🔌 WebSocket地址: ws://localhost:8000/ws/chat/{room_id}/")
print("⏹️  按 Ctrl+C 停止服务器")
print("-" * 50)

# 直接启动daphne
os.system("python -m daphne -b 127.0.0.1 -p 8000 myproject.asgi:application")
