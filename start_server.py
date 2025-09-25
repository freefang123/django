#!/usr/bin/env python
"""
Django聊天服务器启动脚本
支持WebSocket和HTTP API
"""
import os
import sys
import subprocess
import argparse

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

def start_development_server():
    """启动开发服务器"""
    print("🚀 启动Django聊天服务器（开发环境）...")
    print("📡 支持HTTP API和WebSocket连接")
           print("🌐 服务器地址: http://localhost:8000")
           print("🔌 WebSocket地址: ws://localhost:8000/ws/chat/{room_id}/")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        # 检查daphne是否可用
        result = subprocess.run([
            "python", "-m", "daphne", "--help"
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ 错误: daphne模块不可用")
            print("💡 请先安装依赖: pip install -r requirements.txt")
            sys.exit(1)
        
        # 使用daphne启动ASGI服务器
               subprocess.run([
                   "python", "-m", "daphne", 
                   "-b", "127.0.0.1", 
                   "-p", "8000", 
                   "myproject.asgi:application"
               ])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except FileNotFoundError:
        print("❌ 错误: 找不到Python或daphne")
        print("💡 请检查Python环境并安装依赖: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("💡 请检查项目配置和依赖")
        sys.exit(1)

def start_production_server():
    """启动生产服务器"""
    print("🚀 启动Django聊天服务器（生产环境）...")
    print("📡 支持HTTP API和WebSocket连接")
    print("🌐 服务器地址: http://0.0.0.0:8000")
    print("🔌 WebSocket地址: ws://0.0.0.0:8000/ws/chat/{room_id}/")
    print("⏹️  按 Ctrl+C 停止服务器")
    print("-" * 50)
    
    try:
        # 使用daphne启动ASGI服务器
        subprocess.run([
            "python", "-m", "daphne", 
            "-b", "0.0.0.0", 
            "-p", "8000", 
            "myproject.asgi:application"
        ])
    except KeyboardInterrupt:
        print("\n👋 服务器已停止")
    except FileNotFoundError:
        print("❌ 错误: 找不到daphne命令")
        print("💡 请先安装依赖: pip install -r requirements-prod.txt")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Django聊天服务器启动脚本')
    parser.add_argument('--env', choices=['dev', 'prod'], default='dev',
                       help='服务器环境 (默认: dev)')
    
    args = parser.parse_args()
    
    if args.env == 'prod':
        start_production_server()
    else:
        start_development_server()

if __name__ == '__main__':
    main()
