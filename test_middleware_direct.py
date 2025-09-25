#!/usr/bin/env python
"""
直接测试中间件
"""
import asyncio
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

async def test_middleware_direct():
    """直接测试中间件"""
    
    print("🔍 直接测试中间件...")
    
    try:
        # 初始化Django
        import django
        django.setup()
        
        from chat_app.middleware import JWTAuthMiddleware
        from django.contrib.auth.models import AnonymousUser
        
        # 创建中间件实例
        middleware = JWTAuthMiddleware(None)
        
        # 模拟scope
        scope = {
            'type': 'websocket',
            'query_string': b'token=test_token_123',
            'user': AnonymousUser()
        }
        
        print(f"🔍 测试scope: {scope}")
        
        # 测试中间件
        await middleware(scope, None, None)
        
        print(f"✅ 中间件测试完成")
        print(f"🔍 最终scope['user']: {scope.get('user', 'No user')}")
        
    except Exception as e:
        print(f"❌ 中间件测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_middleware_direct())
