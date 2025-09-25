#!/usr/bin/env python
"""
调试WebSocket认证问题
"""
import asyncio
import websockets
import json
import requests

async def test_websocket_auth_debug():
    """调试WebSocket认证"""
    
    print("🔍 调试WebSocket认证...")
    
    # 1. 获取JWT token
    print("\n1. 获取JWT token...")
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
    if response.status_code == 200:
        token_data = response.json()
        token = token_data.get('tokens', {}).get('access')
        print(f"✅ 获取token成功: {token[:50]}...")
    else:
        print(f"❌ 登录失败: {response.status_code}")
        return
    
    # 2. 测试WebSocket连接
    print("\n2. 测试WebSocket连接...")
    uri = f"ws://localhost:8000/ws/chat/2/?token={token}"
    print(f"连接地址: {uri}")
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket连接成功")
            
            # 等待连接确认消息
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 连接确认: {data}")
            
            # 检查是否有用户信息
            if 'user' in data:
                print(f"✅ 连接确认包含用户信息: {data['user']}")
            else:
                print("❌ 连接确认没有用户信息")
            
    except Exception as e:
        print(f"❌ WebSocket连接失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_auth_debug())
