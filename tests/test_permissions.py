#!/usr/bin/env python
"""
Django权限系统测试脚本
"""
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from permission_app.models import UserProfile, PermissionLog

def create_test_data():
    """创建测试数据"""
    print("创建测试数据...")
    
    # 创建测试用户
    user1, created = User.objects.get_or_create(
        username='testuser1',
        defaults={
            'email': 'testuser1@example.com',
            'first_name': 'Test',
            'last_name': 'User1'
        }
    )
    if created:
        user1.set_password('password123')
        user1.save()
        print(f"创建用户: {user1.username}")
    
    user2, created = User.objects.get_or_create(
        username='testuser2',
        defaults={
            'email': 'testuser2@example.com',
            'first_name': 'Test',
            'last_name': 'User2'
        }
    )
    if created:
        user2.set_password('password123')
        user2.save()
        print(f"创建用户: {user2.username}")
    
    # 创建超级用户
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"创建管理员: {admin_user.username}")
    
    # 创建组
    developers_group, created = Group.objects.get_or_create(name='developers')
    if created:
        print(f"创建组: {developers_group.name}")
    
    managers_group, created = Group.objects.get_or_create(name='managers')
    if created:
        print(f"创建组: {managers_group.name}")
    
    # 获取权限
    content_type = ContentType.objects.get_for_model(User)
    permissions = Permission.objects.filter(content_type=content_type)
    
    # 为组分配权限
    developers_group.permissions.set(permissions[:3])  # 分配前3个权限
    managers_group.permissions.set(permissions)  # 分配所有权限
    
    # 将用户分配到组
    user1.groups.add(developers_group)
    user2.groups.add(managers_group)
    
    print(f"用户 {user1.username} 分配到组: {developers_group.name}")
    print(f"用户 {user2.username} 分配到组: {managers_group.name}")
    
    # 创建用户档案
    profile1, created = UserProfile.objects.get_or_create(
        user=user1,
        defaults={
            'phone': '1234567890',
            'department': 'IT',
            'position': 'Developer'
        }
    )
    if created:
        print(f"创建用户档案: {user1.username}")
    
    profile2, created = UserProfile.objects.get_or_create(
        user=user2,
        defaults={
            'phone': '0987654321',
            'department': 'Management',
            'position': 'Manager'
        }
    )
    if created:
        print(f"创建用户档案: {user2.username}")

def test_permissions():
    """测试权限功能"""
    print("\n测试权限功能...")
    
    # 获取用户
    user1 = User.objects.get(username='testuser1')
    user2 = User.objects.get(username='testuser2')
    admin_user = User.objects.get(username='admin')
    
    print(f"\n用户 {user1.username} 的权限:")
    print(f"- 是员工: {user1.is_staff}")
    print(f"- 是超级用户: {user1.is_superuser}")
    print(f"- 所属组: {[group.name for group in user1.groups.all()]}")
    print(f"- 所有权限: {list(user1.get_all_permissions())}")
    
    print(f"\n用户 {user2.username} 的权限:")
    print(f"- 是员工: {user2.is_staff}")
    print(f"- 是超级用户: {user2.is_superuser}")
    print(f"- 所属组: {[group.name for group in user2.groups.all()]}")
    print(f"- 所有权限: {list(user2.get_all_permissions())}")
    
    print(f"\n管理员 {admin_user.username} 的权限:")
    print(f"- 是员工: {admin_user.is_staff}")
    print(f"- 是超级用户: {admin_user.is_superuser}")
    print(f"- 所有权限: {len(admin_user.get_all_permissions())} 个权限")

def test_permission_logs():
    """测试权限日志"""
    print("\n测试权限日志...")
    
    # 创建一些测试日志
    user1 = User.objects.get(username='testuser1')
    
    # 模拟登录日志
    PermissionLog.objects.create(
        user=user1,
        action='login',
        resource='/api/auth/login',
        ip_address='127.0.0.1',
        success=True,
        message='用户登录成功'
    )
    
    # 模拟权限检查日志
    PermissionLog.objects.create(
        user=user1,
        action='access_granted',
        resource='/api/accounts/',
        permission='api.view_account',
        ip_address='127.0.0.1',
        success=True,
        message='权限验证通过'
    )
    
    print("创建权限日志记录")
    
    # 显示最近的日志
    recent_logs = PermissionLog.objects.all()[:5]
    print(f"\n最近的 {len(recent_logs)} 条权限日志:")
    for log in recent_logs:
        print(f"- {log.user.username}: {log.get_action_display()} - {log.resource} ({'成功' if log.success else '失败'})")

def main():
    """主函数"""
    print("Django权限系统测试")
    print("=" * 50)
    
    try:
        # 创建测试数据
        create_test_data()
        
        # 测试权限功能
        test_permissions()
        
        # 测试权限日志
        test_permission_logs()
        
        print("\n" + "=" * 50)
        print("测试完成！")
        print("\n可以使用以下用户登录测试:")
        print("- 用户名: testuser1, 密码: password123 (开发者组)")
        print("- 用户名: testuser2, 密码: password123 (管理员组)")
        print("- 用户名: admin, 密码: admin123 (超级用户)")
        
    except Exception as e:
        print(f"测试过程中出现错误: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
