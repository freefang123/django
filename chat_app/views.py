from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group
from django.db.models import Q, Count, Max
from django.utils import timezone
from .models import ChatRoom, ChatMessage, ChatRoomMember, ChatMessageRead, ChatNotification
from .serializers import (
    ChatRoomSerializer, ChatRoomCreateSerializer, ChatRoomListSerializer,
    ChatMessageSerializer, ChatMessageCreateSerializer,
    ChatRoomMemberSerializer, ChatMessageReadSerializer, ChatNotificationSerializer
)
from .pagination import ChatMessagePagination


class DeveloperPermission(permissions.BasePermission):
    """所有认证用户都可以访问的权限类"""
    
    def has_permission(self, request, view):
        # 只需要用户已认证即可
        return request.user.is_authenticated


class ChatRoomListCreateView(generics.ListCreateAPIView):
    """聊天房间列表和创建视图"""
    permission_classes = [IsAuthenticated, DeveloperPermission]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatRoomCreateSerializer
        return ChatRoomListSerializer
    
    def get_queryset(self):
        # 只返回用户有权限访问的房间，按ID从大到小排列
        return ChatRoom.objects.filter(
            Q(members=self.request.user) | Q(created_by=self.request.user)
        ).distinct().order_by('-id')
    
    def perform_create(self, serializer):
        room = serializer.save()
        # 自动将创建者添加为房间成员
        room.members.add(self.request.user)
        # 创建房间成员记录
        ChatRoomMember.objects.create(
            room=room,
            user=self.request.user,
            role='admin'
        )


class ChatRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    """聊天房间详情视图"""
    permission_classes = [IsAuthenticated, DeveloperPermission]
    serializer_class = ChatRoomSerializer
    
    def get_queryset(self):
        return ChatRoom.objects.filter(
            Q(members=self.request.user) | Q(created_by=self.request.user)
        ).distinct()
    
    def perform_destroy(self, instance):
        # 软删除房间
        instance.is_active = False
        instance.save()


class ChatMessageListCreateView(generics.ListCreateAPIView):
    """聊天消息列表和创建视图"""
    permission_classes = [IsAuthenticated, DeveloperPermission]
    pagination_class = ChatMessagePagination
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ChatMessageCreateSerializer
        return ChatMessageSerializer
    
    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return ChatMessage.objects.filter(
            room_id=room_id,
            room__members=self.request.user,
            is_deleted=False
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        message = serializer.save()
        # 标记消息为已读
        ChatMessageRead.objects.get_or_create(
            message=message,
            user=self.request.user
        )
        # 发送通知给房间其他成员
        self._send_notifications(message)
    
    def _send_notifications(self, message):
        """发送消息通知"""
        room_members = message.room.members.exclude(id=message.sender.id)
        for member in room_members:
            ChatNotification.objects.create(
                user=member,
                notification_type='message',
                title=f'新消息来自 {message.sender.username}',
                content=message.content[:100],
                room=message.room,
                message=message
            )


class ChatRoomMembersView(generics.ListAPIView):
    """房间成员列表视图"""
    permission_classes = [IsAuthenticated, DeveloperPermission]
    serializer_class = ChatRoomMemberSerializer
    
    def get_queryset(self):
        room_id = self.kwargs.get('room_id')
        return ChatRoomMember.objects.filter(
            room_id=room_id,
            room__members=self.request.user
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def join_room(request, room_id):
    """加入房间"""
    try:
        room = ChatRoom.objects.get(id=room_id, is_active=True)
        
        # 检查房间是否已满
        if room.member_count >= room.max_members:
            return Response(
                {'error': '房间已满'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 添加用户到房间
        if not room.members.filter(id=request.user.id).exists():
            room.members.add(request.user)
            ChatRoomMember.objects.create(
                room=room,
                user=request.user,
                role='member'
            )
            
            # 发送系统消息
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message_type='system',
                content=f'{request.user.username} 加入了房间'
            )
        
        return Response({'message': '成功加入房间'})
    
    except ChatRoom.DoesNotExist:
        return Response(
            {'error': '房间不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def leave_room(request, room_id):
    """离开房间"""
    try:
        room = ChatRoom.objects.get(id=room_id)
        
        if room.members.filter(id=request.user.id).exists():
            room.members.remove(request.user)
            ChatRoomMember.objects.filter(
                room=room, 
                user=request.user
            ).delete()
            
            # 发送系统消息
            ChatMessage.objects.create(
                room=room,
                sender=request.user,
                message_type='system',
                content=f'{request.user.username} 离开了房间'
            )
        
        return Response({'message': '成功离开房间'})
    
    except ChatRoom.DoesNotExist:
        return Response(
            {'error': '房间不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def mark_message_read(request, message_id):
    """标记消息为已读"""
    try:
        message = ChatMessage.objects.get(id=message_id)
        
        # 检查用户是否有权限访问该消息
        if not message.room.members.filter(id=request.user.id).exists():
            return Response(
                {'error': '无权限访问该消息'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        ChatMessageRead.objects.get_or_create(
            message=message,
            user=request.user
        )
        
        return Response({'message': '消息已标记为已读'})
    
    except ChatMessage.DoesNotExist:
        return Response(
            {'error': '消息不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def get_notifications(request):
    """获取用户通知"""
    notifications = ChatNotification.objects.filter(
        user=request.user
    ).order_by('-created_at')[:50]
    
    serializer = ChatNotificationSerializer(notifications, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def mark_notification_read(request, notification_id):
    """标记通知为已读"""
    try:
        notification = ChatNotification.objects.get(
            id=notification_id,
            user=request.user
        )
        notification.is_read = True
        notification.save()
        
        return Response({'message': '通知已标记为已读'})
    
    except ChatNotification.DoesNotExist:
        return Response(
            {'error': '通知不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def get_room_messages(request, room_id):
    """获取房间消息历史"""
    try:
        room = ChatRoom.objects.get(id=room_id)
        
        # 检查用户是否有权限访问该房间
        if not room.members.filter(id=request.user.id).exists():
            return Response(
                {'error': '无权限访问该房间'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 获取分页参数
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        
        # 计算偏移量
        offset = (page - 1) * page_size
        
        # 获取消息
        messages = ChatMessage.objects.filter(
            room=room,
            is_deleted=False
        ).order_by('-created_at')[offset:offset + page_size]
        
        serializer = ChatMessageSerializer(messages, many=True)
        
        return Response({
            'messages': serializer.data,
            'page': page,
            'page_size': page_size,
            'total': ChatMessage.objects.filter(room=room, is_deleted=False).count()
        })
    
    except ChatRoom.DoesNotExist:
        return Response(
            {'error': '房间不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated, DeveloperPermission])
def delete_message(request, message_id):
    """删除消息（软删除）"""
    try:
        message = ChatMessage.objects.get(id=message_id)
        
        # 检查用户是否有权限删除该消息
        if message.sender != request.user:
            return Response(
                {'error': '只能删除自己的消息'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        message.soft_delete()
        
        return Response({'message': '消息已删除'})
    
    except ChatMessage.DoesNotExist:
        return Response(
            {'error': '消息不存在'}, 
            status=status.HTTP_404_NOT_FOUND
        )
