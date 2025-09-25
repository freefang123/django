from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthMiddleware(BaseMiddleware):
    """JWT认证中间件"""
    
    async def __call__(self, scope, receive, send):
        print(f"🔍 JWTAuthMiddleware被调用")
        
        # 从查询参数中获取token
        query_string = scope.get('query_string', b'').decode()
        token = None
        
        print(f"🔍 WebSocket query_string: {query_string}")
        
        if query_string:
            params = query_string.split('&')
            for param in params:
                if param.startswith('token='):
                    token = param.split('=')[1]
                    break
        
        print(f"🔍 Extracted token: {token[:50] if token else 'None'}...")
        
        if token:
            try:
                # 验证JWT token
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = await database_sync_to_async(User.objects.get)(id=user_id)
                scope['user'] = user
                print(f"✅ User authenticated: {user.username} (ID: {user.id})")
            except Exception as e:
                print(f"❌ JWT authentication failed: {e}")
                scope['user'] = AnonymousUser()
        else:
            print("❌ No token provided")
            scope['user'] = AnonymousUser()
        
        print(f"🔍 最终scope['user']: {scope.get('user', 'No user')}")
        return await super().__call__(scope, receive, send)
