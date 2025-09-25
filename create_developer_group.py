#!/usr/bin/env python
"""
创建developer用户组并设置权限
"""
import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User, Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def create_developer_group():
    """创建developer用户组"""
    # 创建或获取developer组
    developer_group, created = Group.objects.get_or_create(name='developer')
    
    if created:
        print("✅ 成功创建developer用户组")
    else:
        print("ℹ️ developer用户组已存在")
    
    # 获取聊天相关的权限
    chat_content_type = ContentType.objects.get_for_model(Group)  # 使用Group作为示例
    
    # 为developer组添加所有权限（简化处理）
    all_permissions = Permission.objects.all()
    developer_group.permissions.set(all_permissions)
    
    print(f"✅ 已为developer组分配 {all_permissions.count()} 个权限")
    
    # 创建测试用户（如果不存在）
    test_user, created = User.objects.get_or_create(
        username='developer',
        defaults={
            'email': 'developer@example.com',
            'first_name': 'Developer',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        test_user.set_password('developer123')
        test_user.save()
        print("✅ 创建测试用户: developer / developer123")
    else:
        print("ℹ️ 测试用户已存在: developer")
    
    # 将用户添加到developer组
    test_user.groups.add(developer_group)
    print("✅ 已将测试用户添加到developer组")
    
    return developer_group, test_user

if __name__ == '__main__':
    create_developer_group()
    print("\n🎉 设置完成！")
    print("现在可以使用以下账户测试聊天功能：")
    print("用户名: developer")
    print("密码: developer123")
    print("\n访问聊天页面: http://localhost:8000/api/chat/")
