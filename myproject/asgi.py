"""
ASGI config for myproject project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# 初始化Django应用
django_asgi_app = get_asgi_application()

# 导入WebSocket路由和JWT认证中间件
import chat_app.routing
from chat_app.middleware import JWTAuthMiddleware

# 启用JWT认证的WebSocket配置
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": JWTAuthMiddleware(
        URLRouter(
            chat_app.routing.websocket_urlpatterns
        )
    ),
})
