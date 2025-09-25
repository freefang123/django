#!/usr/bin/env python
"""
简单测试分页功能
"""
import requests
import json

def test_simple_pagination():
    """简单测试分页功能"""
    
    # 获取token
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
    token = response.json().get('tokens', {}).get('access')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # 测试分页
    print("🔍 测试分页功能...")
    
    # 测试第1页，每页5条
    print("\n📄 第1页，每页5条:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/?page=1&page_size=5",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    data = response.json()
    print(f"响应键: {list(data.keys())}")
    
    if 'pagination' in data:
        print(f"分页信息: {data['pagination']}")
    else:
        print("没有分页信息")
    
    print(f"消息数量: {len(data.get('results', []))}")
    
    # 显示消息ID
    messages = data.get('results', [])
    if messages:
        print(f"消息ID: {[msg.get('id') for msg in messages]}")
    
    # 测试第2页
    print("\n📄 第2页，每页5条:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/?page=2&page_size=5",
        headers=headers
    )
    
    print(f"状态码: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"消息数量: {len(data.get('results', []))}")
        messages = data.get('results', [])
        if messages:
            print(f"消息ID: {[msg.get('id') for msg in messages]}")
    else:
        print(f"错误: {response.text}")

if __name__ == "__main__":
    test_simple_pagination()
