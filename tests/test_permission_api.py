#!/usr/bin/env python
"""
Django权限管理API测试脚本
"""
import requests
import json

# API基础URL
BASE_URL = 'http://localhost:8000/api'

def get_auth_token(username, password):
    """获取认证令牌"""
    url = f"{BASE_URL}/auth/login"
    data = {
        'username': username,
        'password': password
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                return result['tokens']['access']
        print(f"登录失败: {response.text}")
        return None
    except Exception as e:
        print(f"登录请求失败: {str(e)}")
        return None

def test_user_permissions(token):
    """测试获取用户权限"""
    print("\n测试获取用户权限...")
    url = f"{BASE_URL}/permission/user-permissions"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"用户权限: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_permission_stats(token):
    """测试权限统计"""
    print("\n测试权限统计...")
    url = f"{BASE_URL}/permission/permission-stats"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"权限统计: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_user_list(token):
    """测试用户列表"""
    print("\n测试用户列表...")
    url = f"{BASE_URL}/permission/users/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"用户列表: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_group_list(token):
    """测试组列表"""
    print("\n测试组列表...")
    url = f"{BASE_URL}/permission/groups/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"组列表: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_permission_list(token):
    """测试权限列表"""
    print("\n测试权限列表...")
    url = f"{BASE_URL}/permission/permissions/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"权限列表: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_permission_logs(token):
    """测试权限日志"""
    print("\n测试权限日志...")
    url = f"{BASE_URL}/permission/logs/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"权限日志: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_protected_api(token):
    """测试受保护的API"""
    print("\n测试受保护的API...")
    
    # 测试需要权限的API
    url = f"{BASE_URL}/accounts/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"账户API状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"账户数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"账户API请求失败: {response.text}")
    except Exception as e:
        print(f"账户API请求失败: {str(e)}")
    
    # 测试需要组的API
    url = f"{BASE_URL}/threading/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.post(url, headers=headers)
        print(f"多线程API状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"多线程数据: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"多线程API请求失败: {response.text}")
    except Exception as e:
        print(f"多线程API请求失败: {str(e)}")

def main():
    """主函数"""
    print("Django权限管理API测试")
    print("=" * 50)
    
    # 测试不同用户的权限
    test_users = [
        ('testuser1', 'password123', '开发者用户'),
        ('testuser2', 'password123', '管理员用户'),
        ('admin', 'admin123', '超级用户')
    ]
    
    for username, password, description in test_users:
        print(f"\n测试 {description} ({username})")
        print("-" * 30)
        
        # 获取认证令牌
        token = get_auth_token(username, password)
        if not token:
            print(f"无法获取 {username} 的认证令牌")
            continue
        
        print(f"成功获取 {username} 的认证令牌")
        
        # 测试各种API
        test_user_permissions(token)
        test_permission_stats(token)
        test_user_list(token)
        test_group_list(token)
        test_permission_list(token)
        test_permission_logs(token)
        test_protected_api(token)
        
        print(f"\n{description} 测试完成")
        print("=" * 50)

if __name__ == '__main__':
    main()
