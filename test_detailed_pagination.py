#!/usr/bin/env python
"""
详细测试分页功能
"""
import requests
import json

def test_detailed_pagination():
    """详细测试分页功能"""
    
    # 获取token
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post("http://localhost:8000/api/auth/login", json=login_data)
    token = response.json().get('tokens', {}).get('access')
    
    headers = {'Authorization': f'Bearer {token}'}
    
    print("🔍 详细测试分页功能...")
    
    # 测试不同的分页参数
    test_cases = [
        {"page": 1, "page_size": 5, "description": "第1页，每页5条"},
        {"page": 2, "page_size": 5, "description": "第2页，每页5条"},
        {"page": 1, "page_size": 10, "description": "第1页，每页10条"},
        {"page": 2, "page_size": 10, "description": "第2页，每页10条"},
        {"page": 1, "page_size": 3, "description": "第1页，每页3条"},
        {"page": 2, "page_size": 3, "description": "第2页，每页3条"},
    ]
    
    for test_case in test_cases:
        print(f"\n📄 {test_case['description']}:")
        
        url = f"http://localhost:8000/api/chat/rooms/2/messages/?page={test_case['page']}&page_size={test_case['page_size']}"
        response = requests.get(url, headers=headers)
        
        print(f"  状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"  响应键: {list(data.keys())}")
            
            # 检查分页信息
            if 'pagination' in data:
                pagination = data['pagination']
                print(f"  📊 分页信息:")
                print(f"    - 当前页: {pagination.get('current_page')}")
                print(f"    - 总页数: {pagination.get('total_pages')}")
                print(f"    - 每页大小: {pagination.get('page_size')}")
                print(f"    - 总记录数: {pagination.get('total_count')}")
                print(f"    - 有下一页: {pagination.get('has_next')}")
                print(f"    - 有上一页: {pagination.get('has_previous')}")
            else:
                print(f"  📊 默认分页信息:")
                print(f"    - 总数: {data.get('count', 'N/A')}")
                print(f"    - 下一页: {data.get('next', 'N/A')}")
                print(f"    - 上一页: {data.get('previous', 'N/A')}")
            
            print(f"  📨 消息数量: {len(data.get('results', []))}")
            
            # 显示消息ID
            messages = data.get('results', [])
            if messages:
                message_ids = [msg.get('id') for msg in messages]
                print(f"  📋 消息ID: {message_ids}")
        else:
            print(f"  ❌ 错误: {response.text}")

if __name__ == "__main__":
    test_detailed_pagination()
