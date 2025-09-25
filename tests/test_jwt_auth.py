#!/usr/bin/env python
"""
JWT认证测试脚本
"""
import requests
import json

def test_jwt_token():
    """测试JWT token获取"""
    print("测试JWT token获取...")
    
    try:
        # 获取JWT token
        url = 'http://localhost:8000/api/token/'
        data = {
            'username': 'admin',
            'password': 'admin123'
        }
        response = requests.post(url, json=data)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            print("✅ JWT token获取成功")
            print(f"Access token: {token_data.get('access', '')[:50]}...")
            return token_data.get('access')
        else:
            print(f"❌ JWT token获取失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
        return None
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return None

def test_user_menu_with_token(token):
    """使用JWT token测试用户菜单API"""
    print("\n测试用户菜单API（带JWT认证）...")
    
    if not token:
        print("❌ 没有有效的JWT token")
        return
    
    try:
        # 使用JWT token访问用户菜单API
        url = 'http://localhost:8000/api/permission/user-menu/'
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = requests.get(url, headers=headers)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            menu_data = response.json()
            print("✅ 用户菜单API访问成功")
            print(f"返回数据: {json.dumps(menu_data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ 用户菜单API访问失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_user_menu_without_token():
    """测试用户菜单API（无认证）"""
    print("\n测试用户菜单API（无认证）...")
    
    try:
        # 不使用JWT token访问用户菜单API
        url = 'http://localhost:8000/api/permission/user-menu/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 401:
            print("✅ 正确返回401未授权错误")
        else:
            print(f"❌ 预期401错误，但得到: {response.status_code}")
            print(f"响应内容: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def main():
    """主函数"""
    print("JWT认证功能测试")
    print("=" * 50)
    
    # 测试JWT token获取
    token = test_jwt_token()
    
    # 测试用户菜单API（带认证）
    test_user_menu_with_token(token)
    
    # 测试用户菜单API（无认证）
    test_user_menu_without_token()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n说明:")
    print("- JWT token获取: 需要有效的用户名和密码")
    print("- 用户菜单API: 需要JWT token认证")
    print("- 无认证访问: 应该返回401错误")

if __name__ == '__main__':
    main()
