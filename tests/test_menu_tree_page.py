#!/usr/bin/env python
"""
菜单树页面测试脚本
"""
import requests
import json

def test_menu_tree_page():
    """测试菜单树页面"""
    print("测试菜单树页面...")
    
    try:
        # 测试菜单树页面
        url = 'http://localhost:8000/api/permission/menu-tree/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 菜单树页面访问成功")
            print(f"页面内容长度: {len(response.text)} 字符")
            
            # 检查页面是否包含关键元素
            content = response.text
            if '菜单树状结构管理' in content:
                print("✅ 页面标题正确")
            if '主菜单' in content:
                print("✅ 菜单数据加载成功")
            if '统计信息' in content:
                print("✅ 统计信息显示正常")
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_menu_tree_api():
    """测试菜单树API"""
    print("\n测试菜单树API...")
    
    try:
        # 测试菜单树API
        url = 'http://localhost:8000/api/permission/menu-tree-api/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ 菜单树API访问成功")
            print(f"返回数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ API访问失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_django_admin():
    """测试Django管理后台"""
    print("\n测试Django管理后台...")
    
    try:
        # 测试Django管理后台
        url = 'http://localhost:8000/admin/permission_app/menuitem/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ Django管理后台访问成功")
        elif response.status_code == 302:
            print("✅ Django管理后台重定向到登录页面（正常）")
        else:
            print(f"❌ 管理后台访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def main():
    """主函数"""
    print("菜单树页面测试")
    print("=" * 50)
    
    # 测试菜单树页面
    test_menu_tree_page()
    
    # 测试菜单树API
    test_menu_tree_api()
    
    # 测试Django管理后台
    test_django_admin()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n访问地址:")
    print("- 菜单树管理页面: http://localhost:8000/api/permission/menu-tree/")
    print("- Django管理后台: http://localhost:8000/admin/permission_app/menuitem/")

if __name__ == '__main__':
    main()
