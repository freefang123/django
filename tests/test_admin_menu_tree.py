#!/usr/bin/env python
"""
Django管理后台菜单树功能测试
"""
import requests
import json

def test_admin_menu_tree():
    """测试Django管理后台菜单树功能"""
    print("测试Django管理后台菜单树功能...")
    
    try:
        # 测试Django管理后台菜单项列表
        url = 'http://localhost:8000/admin/permission_app/menuitem/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ Django管理后台菜单树页面访问成功")
            print(f"页面内容长度: {len(response.text)} 字符")
            
            # 检查页面是否包含关键元素
            content = response.text
            if '菜单树状结构图' in content:
                print("✅ 菜单树标题显示正常")
            if '统计信息' in content:
                print("✅ 统计信息显示正常")
            if '主菜单' in content:
                print("✅ 菜单数据加载成功")
            if '📁' in content or '📄' in content:
                print("✅ 菜单图标显示正常")
            if '编辑' in content and '删除' in content:
                print("✅ 操作按钮显示正常")
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            print(f"错误信息: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_menu_permissions():
    """测试菜单权限管理页面"""
    print("\n测试菜单权限管理页面...")
    
    try:
        url = 'http://localhost:8000/admin/permission_app/menupermission/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 菜单权限管理页面访问成功")
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_menu_logs():
    """测试菜单日志页面"""
    print("\n测试菜单日志页面...")
    
    try:
        url = 'http://localhost:8000/admin/permission_app/usermenulog/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 菜单日志页面访问成功")
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def test_permission_logs():
    """测试权限日志页面"""
    print("\n测试权限日志页面...")
    
    try:
        url = 'http://localhost:8000/admin/permission_app/permissionlog/'
        response = requests.get(url)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("✅ 权限日志页面访问成功")
        else:
            print(f"❌ 页面访问失败: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保Django服务器正在运行")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")

def main():
    """主函数"""
    print("Django管理后台菜单树功能测试")
    print("=" * 50)
    
    # 测试菜单树页面
    test_admin_menu_tree()
    
    # 测试菜单权限管理
    test_menu_permissions()
    
    # 测试菜单日志
    test_menu_logs()
    
    # 测试权限日志
    test_permission_logs()
    
    print("\n" + "=" * 50)
    print("测试完成！")
    print("\n访问地址:")
    print("- 菜单项管理: http://localhost:8000/admin/permission_app/menuitem/")
    print("- 菜单权限管理: http://localhost:8000/admin/permission_app/menupermission/")
    print("- 菜单日志: http://localhost:8000/admin/permission_app/usermenulog/")
    print("- 权限日志: http://localhost:8000/admin/permission_app/permissionlog/")

if __name__ == '__main__':
    main()
