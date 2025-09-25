#!/usr/bin/env python3
"""
JWT认证API测试脚本
用于测试注册、登录、API调用等功能
"""

import requests
import json
import time

# 配置
BASE_URL = "http://localhost:8000"
TEST_USERNAME = "testuser"
TEST_PASSWORD = "testpass123"
TEST_EMAIL = "test@example.com"

def print_response(response, title):
    """打印响应信息"""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"状态码: {response.status_code}")
    print(f"响应内容:")
    try:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except:
        print(response.text)
    print(f"{'='*50}")

def test_register():
    """测试用户注册"""
    url = f"{BASE_URL}/api/auth/register/"
    data = {
        "username": TEST_USERNAME,
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD,
        "confirm_password": TEST_PASSWORD,
        "first_name": "Test",
        "last_name": "User"
    }
    
    response = requests.post(url, json=data)
    print_response(response, "用户注册测试")
    return response.json() if response.status_code == 201 else None

def test_login():
    """测试用户登录"""
    url = f"{BASE_URL}/api/auth/login/"
    data = {
        "username": TEST_USERNAME,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(url, json=data)
    print_response(response, "用户登录测试")
    return response.json() if response.status_code == 200 else None

def test_profile(access_token):
    """测试获取用户档案"""
    url = f"{BASE_URL}/api/auth/profile/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    print_response(response, "获取用户档案测试")
    return response.json() if response.status_code == 200 else None

def test_update_profile(access_token):
    """测试更新用户档案"""
    url = f"{BASE_URL}/api/auth/profile/update/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "phone": "13800138000",
        "avatar": "https://example.com/avatar.jpg"
    }
    
    response = requests.put(url, json=data, headers=headers)
    print_response(response, "更新用户档案测试")
    return response.json() if response.status_code == 200 else None

def test_panda_api(access_token):
    """测试Pandas数据处理API"""
    url = f"{BASE_URL}/api/panda/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    print_response(response, "Pandas数据处理API测试")
    return response.json() if response.status_code == 200 else None

def test_encrypt_api(access_token):
    """测试数据加密API"""
    url = f"{BASE_URL}/api/encrypt/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "phone": "13800138000"
    }
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response, "数据加密API测试")
    return response.json() if response.status_code == 200 else None

def test_multiprocessing_api(access_token):
    """测试多进程处理API"""
    url = f"{BASE_URL}/api/multiprocessing/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    print_response(response, "多进程处理API测试")
    return response.json() if response.status_code == 200 else None

def test_refresh_token(refresh_token):
    """测试刷新令牌"""
    url = f"{BASE_URL}/api/auth/refresh/"
    data = {
        "refresh": refresh_token
    }
    
    response = requests.post(url, json=data)
    print_response(response, "刷新令牌测试")
    return response.json() if response.status_code == 200 else None

def test_logout(access_token, refresh_token):
    """测试用户登出"""
    url = f"{BASE_URL}/api/auth/logout/"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "refresh_token": refresh_token
    }
    
    response = requests.post(url, json=data, headers=headers)
    print_response(response, "用户登出测试")
    return response.json() if response.status_code == 200 else None

def main():
    """主测试函数"""
    print("开始JWT认证API测试...")
    
    # 1. 测试注册
    register_result = test_register()
    if not register_result:
        print("注册失败，跳过后续测试")
        return
    
    # 获取令牌
    access_token = register_result.get('tokens', {}).get('access')
    refresh_token = register_result.get('tokens', {}).get('refresh')
    
    if not access_token:
        print("未获取到访问令牌，跳过后续测试")
        return
    
    # 2. 测试登录
    login_result = test_login()
    if login_result:
        access_token = login_result.get('tokens', {}).get('access')
        refresh_token = login_result.get('tokens', {}).get('refresh')
    
    # 3. 测试获取用户档案
    test_profile(access_token)
    
    # 4. 测试更新用户档案
    test_update_profile(access_token)
    
    # 5. 测试业务API
    test_panda_api(access_token)
    test_encrypt_api(access_token)
    test_multiprocessing_api(access_token)
    
    # 6. 测试刷新令牌
    if refresh_token:
        test_refresh_token(refresh_token)
    
    # 7. 测试登出
    test_logout(access_token, refresh_token)
    
    print("\n测试完成！")

if __name__ == "__main__":
    main() 