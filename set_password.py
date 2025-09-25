#!/usr/bin/env python
"""
设置admin用户密码
"""

import os
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.contrib.auth.models import User

def set_admin_password():
    """设置admin用户密码"""
    try:
        # 获取admin用户
        admin_user = User.objects.get(username='admin')
        
        # 设置密码
        admin_user.set_password('admin123')
        admin_user.save()
        
        print("✅ 成功设置admin用户密码为: admin123")
        print("📝 登录信息:")
        print("  用户名: admin")
        print("  密码: admin123")
        
    except User.DoesNotExist:
        print("❌ admin用户不存在")
    except Exception as e:
        print(f"❌ 设置密码失败: {str(e)}")

if __name__ == "__main__":
    set_admin_password() 