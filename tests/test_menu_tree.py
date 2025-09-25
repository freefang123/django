#!/usr/bin/env python
"""
菜单树管理测试脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from permission_app.models import MenuItem, MenuPermission

def test_menu_tree():
    """测试菜单树结构"""
    print("菜单树结构测试")
    print("=" * 50)
    
    # 获取根菜单
    root_menus = MenuItem.objects.filter(parent__isnull=True).order_by('order')
    
    def print_menu_tree(menus, level=0):
        """打印菜单树"""
        indent = "  " * level
        for menu in menus:
            status = "✅" if menu.is_active else "❌"
            icon = "📁" if menu.menuitem_set.exists() else "📄"
            
            print(f"{indent}{icon} {menu.title} ({menu.name}) - {menu.menu_type} - 排序:{menu.order} - {status}")
            
            if menu.url:
                print(f"{indent}  🔗 链接: {menu.url}")
            if menu.component:
                print(f"{indent}  🧩 组件: {menu.component}")
            if menu.icon:
                print(f"{indent}  🎨 图标: {menu.icon}")
            if menu.description:
                print(f"{indent}  📝 描述: {menu.description}")
            
            # 打印子菜单
            if menu.menuitem_set.exists():
                children = menu.menuitem_set.filter(is_active=True).order_by('order')
                print_menu_tree(children, level + 1)
    
    print_menu_tree(root_menus)
    
    # 统计信息
    total_menus = MenuItem.objects.count()
    active_menus = MenuItem.objects.filter(is_active=True).count()
    root_menus_count = MenuItem.objects.filter(parent__isnull=True).count()
    
    print(f"\n统计信息:")
    print(f"- 总菜单数: {total_menus}")
    print(f"- 激活菜单: {active_menus}")
    print(f"- 根菜单数: {root_menus_count}")

def test_menu_permissions():
    """测试菜单权限"""
    print("\n菜单权限测试")
    print("=" * 50)
    
    # 获取菜单权限
    menu_permissions = MenuPermission.objects.select_related('menu', 'group', 'user')
    
    print("菜单权限配置:")
    for mp in menu_permissions:
        if mp.group:
            print(f"- {mp.menu.title} -> 组: {mp.group.name}")
        elif mp.user:
            print(f"- {mp.menu.title} -> 用户: {mp.user.username}")
        elif mp.permission:
            print(f"- {mp.menu.title} -> 权限: {mp.permission}")
    
    # 测试用户菜单权限
    try:
        user1 = User.objects.get(username='testuser1')  # 开发者
        user2 = User.objects.get(username='testuser2')  # 经理
        
        print(f"\n用户 {user1.username} 的菜单权限:")
        from permission_app.views import get_user_menus
        user1_menus = get_user_menus(user1)
        for menu in user1_menus:
            print(f"  - {menu['title']} ({menu['name']})")
            for child in menu.get('children', []):
                print(f"    - {child['title']} ({child['name']})")
        
        print(f"\n用户 {user2.username} 的菜单权限:")
        user2_menus = get_user_menus(user2)
        for menu in user2_menus:
            print(f"  - {menu['title']} ({menu['name']})")
            for child in menu.get('children', []):
                print(f"    - {child['title']} ({child['name']})")
                
    except User.DoesNotExist:
        print("测试用户不存在，请先运行 init_menu_data.py")

def test_menu_api():
    """测试菜单API"""
    print("\n菜单API测试")
    print("=" * 50)
    
    try:
        import requests
        
        # 测试获取菜单树API
        url = 'http://localhost:8000/api/permission/menu-tree-api/'
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            print("菜单树API响应:")
            print(f"- 成功: {data.get('success')}")
            print(f"- 菜单数量: {len(data.get('data', []))}")
            
            for menu in data.get('data', []):
                print(f"  - {menu['title']} ({menu['name']})")
                for child in menu.get('children', []):
                    print(f"    - {child['title']} ({child['name']})")
        else:
            print(f"API请求失败: {response.status_code}")
            
    except ImportError:
        print("requests库未安装，跳过API测试")
    except Exception as e:
        print(f"API测试失败: {str(e)}")

def main():
    """主函数"""
    print("菜单树管理测试")
    print("=" * 50)
    
    try:
        # 测试菜单树结构
        test_menu_tree()
        
        # 测试菜单权限
        test_menu_permissions()
        
        # 测试菜单API
        test_menu_api()
        
        print("\n" + "=" * 50)
        print("测试完成！")
        print("\n访问菜单树管理页面:")
        print("http://localhost:8000/api/permission/menu-tree/")
        print("\n访问Django管理后台:")
        print("http://localhost:8000/admin/permission_app/menuitem/")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
