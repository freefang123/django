#!/usr/bin/env python
"""
最终测试分页功能
"""
import requests
import json

def test_final_pagination():
    """最终测试分页功能"""
    
    # 获取token
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
    token = response.json().get('tokens', {}).get('access')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("🔍 最终测试分页功能...")
    
    # 测试第1页，每页3条
    print("\n📄 第1页，每页3条:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/?page=1&page_size=3",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"响应键: {list(data.keys())}")
        
        # 检查是否有自定义分页格式
        if 'pagination' in data:
            print(f"✅ 自定义分页格式:")
            print(f"  {json.dumps(data['pagination'], indent=2)}")
        else:
            print(f"❌ 使用默认分页格式:")
            print(f"  count: {data.get('count')}")
            print(f"  next: {data.get('next')}")
            print(f"  previous: {data.get('previous')}")
        
        print(f"消息数量: {len(data.get('results', []))}")
        messages = data.get('results', [])
        if messages:
            message_ids = [msg.get('id') for msg in messages]
            print(f"消息ID: {message_ids}")
    
    # 测试第2页，每页3条
    print("\n📄 第2页，每页3条:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/?page=2&page_size=3",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"消息数量: {len(data.get('results', []))}")
        messages = data.get('results', [])
        if messages:
            message_ids = [msg.get('id') for msg in messages]
            print(f"消息ID: {message_ids}")
    else:
        print(f"错误: {response.text}")

if __name__ == "__main__":
    test_final_pagination()
