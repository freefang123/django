#!/usr/bin/env python
"""
菜单API测试脚本
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

def test_user_menu(token, username):
    """测试获取用户菜单"""
    print(f"\n测试用户 {username} 的菜单...")
    url = f"{BASE_URL}/permission/user-menu"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"用户菜单: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_menu_list(token):
    """测试菜单列表"""
    print("\n测试菜单列表...")
    url = f"{BASE_URL}/permission/menus/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"菜单列表: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_menu_tree(token):
    """测试菜单树"""
    print("\n测试菜单树...")
    url = f"{BASE_URL}/permission/menus/tree/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"菜单树: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_menu_permissions(token):
    """测试菜单权限"""
    print("\n测试菜单权限...")
    url = f"{BASE_URL}/permission/menu-permissions/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"菜单权限: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_menu_logs(token):
    """测试菜单日志"""
    print("\n测试菜单日志...")
    url = f"{BASE_URL}/permission/menu-logs/"
    headers = {'Authorization': f'Bearer {token}'}
    
    try:
        response = requests.get(url, headers=headers)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"菜单日志: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def test_log_menu_access(token, menu_id):
    """测试记录菜单访问"""
    print(f"\n测试记录菜单访问 (菜单ID: {menu_id})...")
    url = f"{BASE_URL}/permission/log-menu-access/"
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'menu_id': menu_id,
        'action': 'access'
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"访问记录: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"请求失败: {response.text}")
    except Exception as e:
        print(f"请求失败: {str(e)}")

def main():
    """主函数"""
    print("菜单API测试")
    print("=" * 50)
    
    # 测试不同用户的菜单权限
    test_users = [
        ('testuser1', 'password123', '开发者用户'),
        ('testuser2', 'password123', '经理用户'),
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
        test_user_menu(token, username)
        test_menu_list(token)
        test_menu_tree(token)
        test_menu_permissions(token)
        test_menu_logs(token)
        
        # 测试记录菜单访问
        test_log_menu_access(token, 1)  # 测试访问主菜单
        
        print(f"\n{description} 测试完成")
        print("=" * 50)

if __name__ == '__main__':
    main()
