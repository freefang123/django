#!/usr/bin/env python
"""
菜单数据初始化脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from permission_app.models import MenuItem, MenuPermission

def create_menu_data():
    """创建菜单数据"""
    print("创建菜单数据...")
    
    # 创建主菜单
    main_menu = MenuItem.objects.create(
        name='main',
        title='主菜单',
        icon='menu',
        menu_type='menu',
        order=0,
        is_active=True
    )
    print(f"创建主菜单: {main_menu.title}")
    
    # 创建人员设置菜单
    personnel_menu = MenuItem.objects.create(
        name='personnel',
        title='人员设置',
        icon='users',
        url='/personnel',
        component='PersonnelManagement',
        menu_type='menu',
        parent=main_menu,
        order=1,
        is_active=True,
        description='人员管理相关功能'
    )
    print(f"创建人员设置菜单: {personnel_menu.title}")
    
    # 创建在线聊天菜单
    chat_menu = MenuItem.objects.create(
        name='chat',
        title='在线聊天',
        icon='message-circle',
        url='/chat',
        component='ChatRoom',
        menu_type='menu',
        parent=main_menu,
        order=2,
        is_active=True,
        description='在线聊天功能'
    )
    print(f"创建在线聊天菜单: {chat_menu.title}")
    
    # 创建子菜单
    personnel_submenu1 = MenuItem.objects.create(
        name='personnel_list',
        title='人员列表',
        icon='list',
        url='/personnel/list',
        component='PersonnelList',
        menu_type='submenu',
        parent=personnel_menu,
        order=1,
        is_active=True
    )
    print(f"创建人员列表子菜单: {personnel_submenu1.title}")
    
    personnel_submenu2 = MenuItem.objects.create(
        name='personnel_add',
        title='添加人员',
        icon='plus',
        url='/personnel/add',
        component='PersonnelAdd',
        menu_type='submenu',
        parent=personnel_menu,
        order=2,
        is_active=True
    )
    print(f"创建添加人员子菜单: {personnel_submenu2.title}")
    
    chat_submenu1 = MenuItem.objects.create(
        name='chat_room',
        title='聊天室',
        icon='message-square',
        url='/chat/room',
        component='ChatRoom',
        menu_type='submenu',
        parent=chat_menu,
        order=1,
        is_active=True
    )
    print(f"创建聊天室子菜单: {chat_submenu1.title}")
    
    chat_submenu2 = MenuItem.objects.create(
        name='chat_history',
        title='聊天记录',
        icon='history',
        url='/chat/history',
        component='ChatHistory',
        menu_type='submenu',
        parent=chat_menu,
        order=2,
        is_active=True
    )
    print(f"创建聊天记录子菜单: {chat_submenu2.title}")
    
    return main_menu, personnel_menu, chat_menu

def assign_menu_permissions():
    """分配菜单权限"""
    print("\n分配菜单权限...")
    
    # 获取组
    try:
        managers_group = Group.objects.get(name='managers')
        developers_group = Group.objects.get(name='developers')
    except Group.DoesNotExist:
        print("请先运行 test_permissions.py 创建测试数据")
        return
    
    # 获取菜单
    personnel_menu = MenuItem.objects.get(name='personnel')
    chat_menu = MenuItem.objects.get(name='chat')
    
    # 为经理组分配所有菜单权限
    MenuPermission.objects.create(
        menu=personnel_menu,
        group=managers_group,
        is_active=True
    )
    MenuPermission.objects.create(
        menu=chat_menu,
        group=managers_group,
        is_active=True
    )
    print(f"为经理组 {managers_group.name} 分配所有菜单权限")
    
    # 为开发者组只分配聊天菜单权限
    MenuPermission.objects.create(
        menu=chat_menu,
        group=developers_group,
        is_active=True
    )
    print(f"为开发者组 {developers_group.name} 分配聊天菜单权限")
    
    # 为超级用户分配所有菜单权限
    try:
        admin_user = User.objects.get(username='admin')
        MenuPermission.objects.create(
            menu=personnel_menu,
            user=admin_user,
            is_active=True
        )
        MenuPermission.objects.create(
            menu=chat_menu,
            user=admin_user,
            is_active=True
        )
        print(f"为超级用户 {admin_user.username} 分配所有菜单权限")
    except User.DoesNotExist:
        print("超级用户不存在")

def test_menu_permissions():
    """测试菜单权限"""
    print("\n测试菜单权限...")
    
    # 测试经理用户
    try:
        user1 = User.objects.get(username='testuser2')  # 经理用户
        print(f"\n用户 {user1.username} 的菜单权限:")
        
        # 获取用户菜单
        from permission_app.views import get_user_menus
        user_menus = get_user_menus(user1)
        
        for menu in user_menus:
            print(f"- {menu['title']} ({menu['name']})")
            for child in menu.get('children', []):
                print(f"  - {child['title']} ({child['name']})")
    except User.DoesNotExist:
        print("经理用户不存在")
    
    # 测试开发者用户
    try:
        user2 = User.objects.get(username='testuser1')  # 开发者用户
        print(f"\n用户 {user2.username} 的菜单权限:")
        
        # 获取用户菜单
        from permission_app.views import get_user_menus
        user_menus = get_user_menus(user2)
        
        for menu in user_menus:
            print(f"- {menu['title']} ({menu['name']})")
            for child in menu.get('children', []):
                print(f"  - {child['title']} ({child['name']})")
    except User.DoesNotExist:
        print("开发者用户不存在")

def main():
    """主函数"""
    print("菜单数据初始化")
    print("=" * 50)
    
    try:
        # 创建菜单数据
        create_menu_data()
        
        # 分配菜单权限
        assign_menu_permissions()
        
        # 测试菜单权限
        test_menu_permissions()
        
        print("\n" + "=" * 50)
        print("菜单数据初始化完成！")
        print("\n菜单权限分配:")
        print("- 经理组 (managers): 人员设置 + 在线聊天")
        print("- 开发者组 (developers): 仅在线聊天")
        print("- 超级用户 (admin): 所有菜单")
        
    except Exception as e:
        print(f"初始化过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
