#!/usr/bin/env python
"""
测试认证后的WebSocket连接
"""
import asyncio
import websockets
import json
import requests

# 测试配置
BASE_URL = "http://localhost:8000"
WEBSOCKET_URL = "ws://localhost:8000/ws/chat/2/"

async def test_authenticated_websocket():
    """测试认证后的WebSocket连接"""
    
    print("🔍 测试认证后的WebSocket连接...")
    
    # 1. 获取JWT token
    print("\n1. 获取JWT token...")
    try:
        # 这里需要替换为实际的登录API
        login_data = {
            "username": "admin",  # 替换为实际用户名
            "password": "admin123"  # 替换为实际密码
        }
        
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"登录响应状态: {response.status_code}")
        print(f"登录响应内容: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"Token数据: {token_data}")
            token = token_data.get('tokens', {}).get('access')
            if token:
                print(f"✅ 获取token成功: {token[:50]}...")
            else:
                print(f"❌ 响应中没有access字段")
                return
        else:
            print(f"❌ 登录失败: {response.status_code}")
            return
            
    except Exception as e:
        print(f"❌ 获取token失败: {e}")
        return
    
    # 2. 测试WebSocket连接（带认证）
    print("\n2. 测试WebSocket连接（带认证）...")
    try:
        uri = f"{WEBSOCKET_URL}?token={token}"
        print(f"连接地址: {uri}")
        
        async with websockets.connect(uri) as websocket:
            print("✅ WebSocket连接成功")
            
            # 接收连接确认消息
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 收到连接确认: {data}")
            
            # 发送聊天消息
            print("\n3. 发送聊天消息...")
            message = {
                "type": "chat_message",
                "content": "测试认证用户消息",
                "message_type": "text"
            }
            
            await websocket.send(json.dumps(message))
            print(f"📤 发送消息: {message}")
            
            # 接收消息响应
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 收到响应: {data}")
            
            # 检查消息中的用户信息
            if 'message' in data and 'sender' in data['message']:
                sender = data['message']['sender']
                print(f"✅ 发送者信息: ID={sender.get('id')}, username={sender.get('username')}")
                
                if sender.get('id') != 6:  # 不是匿名用户
                    print("✅ 成功获取真实用户ID!")
                else:
                    print("❌ 仍然是匿名用户")
            else:
                print("❌ 响应中没有用户信息")
                
    except Exception as e:
        print(f"❌ WebSocket连接失败: {e}")
        return
    
    # 3. 测试无认证连接（应该失败）
    print("\n4. 测试无认证连接（应该失败）...")
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("❌ 无认证连接不应该成功")
    except Exception as e:
        print(f"✅ 无认证连接正确被拒绝: {e}")

if __name__ == "__main__":
    asyncio.run(test_authenticated_websocket())
