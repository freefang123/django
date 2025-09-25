from django.urls import re_path
from . import consumers
from . import simple_consumer

websocket_urlpatterns = [
    re_path(r'^ws/chat/(?P<room_id>\w+)/$', simple_consumer.SimpleChatConsumer.as_asgi()),
]
