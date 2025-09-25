import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import ChatRoom, ChatMessage

class SimpleChatConsumer(AsyncWebsocketConsumer):
    """简单的聊天WebSocket消费者"""
    
    async def connect(self):
        """连接WebSocket"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        print(f"🔍 WebSocket connecting to room {self.room_id}")
        
        # 检查用户认证
        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            print(f"❌ 用户未认证，拒绝连接")
            await self.close()
            return
        
        print(f"✅ 认证用户: ID={user.id}, username={user.username}")
        
        # 加入房间组
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # 发送连接成功消息
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': '连接成功',
            'user': {
                'id': user.id,
                'username': user.username
            }
        }))
    
    async def disconnect(self, close_code):
        """断开WebSocket连接"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """接收WebSocket消息"""
        print(f"🔍 收到消息: {text_data}")
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            print(f"🔍 消息类型: {message_type}")
            
            if message_type == 'chat_message':
                print("🔍 处理聊天消息")
                await self.handle_chat_message(data)
            else:
                print(f"🔍 未知消息类型: {message_type}")
            
        except json.JSONDecodeError as e:
            print(f"🔍 JSON解析错误: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '无效的JSON格式'
            }))
        except Exception as e:
            print(f"🔍 处理消息时发生错误: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'处理消息时发生错误: {str(e)}'
            }))
    
    async def handle_chat_message(self, data):
        """处理聊天消息"""
        content = data.get('content', '').strip()
        
        if not content:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '消息内容不能为空'
            }))
            return
        
        # 获取用户信息
        user = self.scope.get('user')
        if user and hasattr(user, 'id') and user.is_authenticated:
            user_id = user.id
            username = user.username
            print(f"✅ 认证用户: ID={user_id}, username={username}")
        else:
            # 如果没有认证用户，拒绝连接
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': '需要用户认证才能发送消息'
            }))
            return
        
        print(f"🔍 用户信息: ID={user_id}, username={username}")
        
        # 保存消息到数据库
        try:
            # 获取房间
            room = await self.get_room(self.room_id)
            if not room:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': '房间不存在'
                }))
                return
            
            # 获取用户
            user_obj = await self.get_user(user_id)
            if not user_obj:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': '用户不存在'
                }))
                return
            
            # 创建消息
            message = await self.create_message(
                room=room,
                sender=user_obj,
                content=content,
                message_type=data.get('message_type', 'text')
            )
            
            print(f"🔍 数据库消息ID: {message.id}")
            
            # 创建消息对象
            message_obj = {
                'id': message.id,  # 使用数据库ID
                'content': content,
                'message_type': data.get('message_type', 'text'),
                'timestamp': message.created_at.isoformat(),
                'sender': {
                    'id': user_id,
                    'username': username
                }
            }
            print(f"🔍 消息对象: {message_obj}")
            
            # 广播消息给房间所有成员
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_obj
                }
            )
            
        except Exception as e:
            print(f"🔍 保存消息时发生错误: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': f'保存消息失败: {str(e)}'
            }))
    
    @database_sync_to_async
    def get_room(self, room_id):
        """获取房间"""
        try:
            return ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return None
    
    @database_sync_to_async
    def get_user(self, user_id):
        """获取用户"""
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
    
    @database_sync_to_async
    def create_message(self, room, sender, content, message_type):
        """创建消息"""
        return ChatMessage.objects.create(
            room=room,
            sender=sender,
            content=content,
            message_type=message_type
        )
    
    @database_sync_to_async
    def get_or_create_default_user(self):
        """获取或创建默认用户"""
        user, created = User.objects.get_or_create(
            username='anonymous',
            defaults={
                'email': 'anonymous@example.com',
                'first_name': 'Anonymous',
                'last_name': 'User'
            }
        )
        return user.id
    
    async def chat_message(self, event):
        """发送聊天消息"""
        message = event['message']
        
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message
        }))
