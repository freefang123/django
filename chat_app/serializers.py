from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage, ChatRoomMember, ChatMessageRead, ChatNotification


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ChatRoomSerializer(serializers.ModelSerializer):
    """聊天房间序列化器"""
    created_by = UserSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    members = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'description', 'room_type', 'created_by', 
            'members', 'member_count', 'is_active', 'max_members', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ChatRoomCreateSerializer(serializers.ModelSerializer):
    """创建聊天房间序列化器"""
    class Meta:
        model = ChatRoom
        fields = ['name', 'description', 'room_type', 'max_members']
    
    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class ChatMessageSerializer(serializers.ModelSerializer):
    """聊天消息序列化器"""
    sender = UserSerializer(read_only=True)
    room = ChatRoomSerializer(read_only=True)
    reply_to = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'room', 'sender', 'message_type', 'content', 
            'file_url', 'file_name', 'file_size', 'is_edited', 
            'is_deleted', 'reply_to', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_reply_to(self, obj):
        if obj.reply_to:
            return {
                'id': obj.reply_to.id,
                'content': obj.reply_to.content[:100],
                'sender': obj.reply_to.sender.username,
                'created_at': obj.reply_to.created_at
            }
        return None


class ChatMessageCreateSerializer(serializers.ModelSerializer):
    """创建聊天消息序列化器"""
    sender = UserSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message_type', 'content', 'file_url', 'file_name', 'file_size', 'reply_to', 'created_at']
        read_only_fields = ['id', 'sender', 'created_at']
    
    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        # 从URL中获取room_id
        room_id = self.context['view'].kwargs.get('room_id')
        from chat_app.models import ChatRoom
        validated_data['room'] = ChatRoom.objects.get(id=room_id)
        return super().create(validated_data)


class ChatRoomMemberSerializer(serializers.ModelSerializer):
    """房间成员序列化器"""
    user = UserSerializer(read_only=True)
    room = ChatRoomSerializer(read_only=True)
    
    class Meta:
        model = ChatRoomMember
        fields = [
            'id', 'room', 'user', 'role', 'joined_at', 
            'last_read_at', 'is_muted', 'is_banned'
        ]
        read_only_fields = ['id', 'joined_at']


class ChatMessageReadSerializer(serializers.ModelSerializer):
    """消息已读状态序列化器"""
    user = UserSerializer(read_only=True)
    message = ChatMessageSerializer(read_only=True)
    
    class Meta:
        model = ChatMessageRead
        fields = ['id', 'message', 'user', 'read_at']
        read_only_fields = ['id', 'read_at']


class ChatNotificationSerializer(serializers.ModelSerializer):
    """聊天通知序列化器"""
    room = ChatRoomSerializer(read_only=True)
    message = ChatMessageSerializer(read_only=True)
    
    class Meta:
        model = ChatNotification
        fields = [
            'id', 'notification_type', 'title', 'content', 
            'room', 'message', 'is_read', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ChatRoomListSerializer(serializers.ModelSerializer):
    """房间列表序列化器（简化版）"""
    created_by = UserSerializer(read_only=True)
    member_count = serializers.ReadOnlyField()
    last_message = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'description', 'room_type', 'created_by', 
            'member_count', 'last_message', 'created_at'
        ]
    
    def get_last_message(self, obj):
        last_msg = obj.messages.filter(is_deleted=False).first()
        if last_msg:
            return {
                'id': last_msg.id,
                'content': last_msg.content[:100],
                'sender': last_msg.sender.username,
                'created_at': last_msg.created_at
            }
        return None
