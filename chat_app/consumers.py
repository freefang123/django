import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatMessage, ChatNotification

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """聊天WebSocket消费者"""
    
    async def connect(self):
        """连接WebSocket"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        # 检查用户是否已认证
        user = self.scope['user']
        if not user.is_authenticated:
            await self.close()
            return
        
        # 检查用户是否有权限访问该房间
        if not await self.has_room_permission(user, self.room_id):
            await self.close()
            return
        
        # 加入房间组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # 发送连接成功消息
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': '连接成功'
        }))
    
    async def disconnect(self, close_code):
        """断开WebSocket连接"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """接收WebSocket消息"""
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'chat_message':
                await self.handle_chat_message(data)
            elif message_type == 'typing':
                await self.handle_typing(data)
            elif message_type == 'user_join':
                await self.handle_user_join(data)
            elif message_type == 'user_leave':
                await self.handle_user_leave(data)
            
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '无效的JSON格式'
            }))
    
    async def handle_chat_message(self, data):
        """处理聊天消息"""
        user = self.scope['user']
        content = data.get('content', '').strip()
        message_type = data.get('message_type', 'text')
        reply_to_id = data.get('reply_to')
        
        if not content:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '消息内容不能为空'
            }))
            return
        
        # 保存消息到数据库
        message = await self.save_message(
            user, self.room_id, content, message_type, reply_to_id
        )
        
        if message:
            # 广播消息给房间所有成员
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': message.id,
                        'sender': {
                            'id': user.id,
                            'username': user.username,
                            'first_name': user.first_name,
                            'last_name': user.last_name
                        },
                        'content': message.content,
                        'message_type': message.message_type,
                        'created_at': message.created_at.isoformat(),
                        'reply_to': message.reply_to_id
                    }
                }
            )
            
            # 发送通知给房间其他成员
            await self.send_notifications(message)
    
    async def handle_typing(self, data):
        """处理正在输入状态"""
        user = self.scope['user']
        is_typing = data.get('is_typing', False)
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'typing',
                'user': {
                    'id': user.id,
                    'username': user.username
                },
                'is_typing': is_typing
            }
        )
    
    async def handle_user_join(self, data):
        """处理用户加入"""
        user = self.scope['user']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_join',
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            }
        )
    
    async def handle_user_leave(self, data):
        """处理用户离开"""
        user = self.scope['user']
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_leave',
                'user': {
                    'id': user.id,
                    'username': user.username
                }
            }
        )
    
    async def chat_message(self, event):
        """发送聊天消息"""
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))
    
    async def typing(self, event):
        """发送正在输入状态"""
        user = event['user']
        is_typing = event['is_typing']
        
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'user': user,
            'is_typing': is_typing
        }))
    
    async def user_join(self, event):
        """发送用户加入消息"""
        user = event['user']
        
        await self.send(text_data=json.dumps({
            'type': 'user_join',
            'user': user
        }))
    
    async def user_leave(self, event):
        """发送用户离开消息"""
        user = event['user']
        
        await self.send(text_data=json.dumps({
            'type': 'user_leave',
            'user': user
        }))
    
    
    @database_sync_to_async
    def has_room_permission(self, user, room_id):
        """检查用户是否有房间权限"""
        try:
            room = ChatRoom.objects.get(id=room_id, is_active=True)
            return room.members.filter(id=user.id).exists()
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, user, room_id, content, message_type, reply_to_id):
        """保存消息到数据库"""
        try:
            room = ChatRoom.objects.get(id=room_id)
            reply_to = None
            
            if reply_to_id:
                try:
                    reply_to = ChatMessage.objects.get(id=reply_to_id, room=room)
                except ChatMessage.DoesNotExist:
                    pass
            
            message = ChatMessage.objects.create(
                room=room,
                sender=user,
                content=content,
                message_type=message_type,
                reply_to=reply_to
            )
            
            return message
        except ChatRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def send_notifications(self, message):
        """发送通知给房间其他成员"""
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
