#!/usr/bin/env python
"""
测试聊天消息分页功能（新版本）
"""
import requests
import json

def test_message_pagination():
    """测试消息分页功能"""
    
    print("🔍 测试聊天消息分页功能...")
    
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
    
    # 2. 测试分页参数
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    print("\n2. 测试分页参数...")
    
    # 测试第1页，每页10条
    print("\n📄 测试第1页，每页10条:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/?page=1&page_size=10",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 状态码: {response.status_code}")
        
        # 检查新的分页格式
        if 'pagination' in data:
            pagination = data['pagination']
            print(f"📊 分页信息:")
            print(f"  - 当前页: {pagination.get('current_page', 'N/A')}")
            print(f"  - 总页数: {pagination.get('total_pages', 'N/A')}")
            print(f"  - 每页大小: {pagination.get('page_size', 'N/A')}")
            print(f"  - 总记录数: {pagination.get('total_count', 'N/A')}")
            print(f"  - 有下一页: {pagination.get('has_next', 'N/A')}")
            print(f"  - 有上一页: {pagination.get('has_previous', 'N/A')}")
            print(f"  - 下一页: {pagination.get('next_page', 'N/A')}")
            print(f"  - 上一页: {pagination.get('previous_page', 'N/A')}")
        else:
            print(f"📊 分页信息: 未找到分页信息")
        
        print(f"  - 消息数量: {len(data.get('results', []))}")
        
        # 显示前几条消息
        messages = data.get('results', [])
        if messages:
            print(f"📨 前3条消息:")
            for i, msg in enumerate(messages[:3]):
                print(f"  {i+1}. ID={msg.get('id')}, 内容={msg.get('content', '')[:20]}...")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"响应: {response.text}")
    
    # 测试第2页
    print("\n📄 测试第2页，每页10条:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/?page=2&page_size=10",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 状态码: {response.status_code}")
        
        if 'pagination' in data:
            pagination = data['pagination']
            print(f"📊 分页信息:")
            print(f"  - 当前页: {pagination.get('current_page', 'N/A')}")
            print(f"  - 总页数: {pagination.get('total_pages', 'N/A')}")
            print(f"  - 每页大小: {pagination.get('page_size', 'N/A')}")
            print(f"  - 总记录数: {pagination.get('total_count', 'N/A')}")
            print(f"  - 有下一页: {pagination.get('has_next', 'N/A')}")
            print(f"  - 有上一页: {pagination.get('has_previous', 'N/A')}")
            print(f"  - 下一页: {pagination.get('next_page', 'N/A')}")
            print(f"  - 上一页: {pagination.get('previous_page', 'N/A')}")
        
        print(f"  - 消息数量: {len(data.get('results', []))}")
        
        # 显示前几条消息
        messages = data.get('results', [])
        if messages:
            print(f"📨 前3条消息:")
            for i, msg in enumerate(messages[:3]):
                print(f"  {i+1}. ID={msg.get('id')}, 内容={msg.get('content', '')[:20]}...")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"响应: {response.text}")
    
    # 测试默认分页（不指定参数）
    print("\n📄 测试默认分页:")
    response = requests.get(
        "http://localhost:8000/api/chat/rooms/2/messages/",
        headers=headers
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ 状态码: {response.status_code}")
        
        if 'pagination' in data:
            pagination = data['pagination']
            print(f"📊 分页信息:")
            print(f"  - 当前页: {pagination.get('current_page', 'N/A')}")
            print(f"  - 总页数: {pagination.get('total_pages', 'N/A')}")
            print(f"  - 每页大小: {pagination.get('page_size', 'N/A')}")
            print(f"  - 总记录数: {pagination.get('total_count', 'N/A')}")
            print(f"  - 有下一页: {pagination.get('has_next', 'N/A')}")
            print(f"  - 有上一页: {pagination.get('has_previous', 'N/A')}")
            print(f"  - 下一页: {pagination.get('next_page', 'N/A')}")
            print(f"  - 上一页: {pagination.get('previous_page', 'N/A')}")
        
        print(f"  - 消息数量: {len(data.get('results', []))}")
    else:
        print(f"❌ 请求失败: {response.status_code}")
        print(f"响应: {response.text}")

if __name__ == "__main__":
    test_message_pagination()
