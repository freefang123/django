#!/usr/bin/env python
"""
简单测试WebSocket连接
"""
import asyncio
import websockets
import json

async def test_websocket_simple():
    """简单测试WebSocket连接"""
    
    print("🔍 简单测试WebSocket连接...")
    
    # 测试无认证连接（应该失败）
    print("\n1. 测试无认证连接（应该失败）...")
    try:
        async with websockets.connect("ws://localhost:8000/ws/chat/2/") as websocket:
            print("❌ 无认证连接不应该成功")
    except Exception as e:
        print(f"✅ 无认证连接正确被拒绝: {e}")
    
    # 测试带token连接
    print("\n2. 测试带token连接...")
    try:
        async with websockets.connect("ws://localhost:8000/ws/chat/2/?token=test_token") as websocket:
            print("✅ 带token连接成功")
            
            # 接收消息
            response = await websocket.recv()
            data = json.loads(response)
            print(f"📨 收到消息: {data}")
            
    except Exception as e:
        print(f"❌ 带token连接失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_websocket_simple())
