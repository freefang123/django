#!/usr/bin/env python
"""
测试ASGI导入
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

try:
    print("🔍 测试ASGI导入...")
    
    # 测试导入
    from myproject.asgi import application
    print("✅ ASGI应用导入成功")
    
    # 测试中间件导入
    from chat_app.middleware import JWTAuthMiddleware
    print("✅ JWTAuthMiddleware导入成功")
    
    # 测试路由导入
    import chat_app.routing
    print("✅ 路由导入成功")
    
    print("✅ 所有导入都成功")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
