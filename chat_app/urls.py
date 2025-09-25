from django.urls import path
from . import views
from . import api_test_views

urlpatterns = [
    # API测试页面
    path('test/', api_test_views.api_test_page, name='api-test-page'),
    
    # 房间相关
    path('rooms/', views.ChatRoomListCreateView.as_view(), name='chat-room-list-create'),
    path('rooms/<int:pk>/', views.ChatRoomDetailView.as_view(), name='chat-room-detail'),
    path('rooms/<int:room_id>/join/', views.join_room, name='join-room'),
    path('rooms/<int:room_id>/leave/', views.leave_room, name='leave-room'),
    path('rooms/<int:room_id>/members/', views.ChatRoomMembersView.as_view(), name='room-members'),
    
    # 消息相关
    path('rooms/<int:room_id>/messages/', views.ChatMessageListCreateView.as_view(), name='message-list-create'),
    path('messages/<int:message_id>/read/', views.mark_message_read, name='mark-message-read'),
    path('messages/<int:message_id>/delete/', views.delete_message, name='delete-message'),
    
    # 通知相关
    path('notifications/', views.get_notifications, name='get-notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
]
