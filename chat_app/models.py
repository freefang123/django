from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class ChatRoom(models.Model):
    """聊天房间模型"""
    ROOM_TYPE_CHOICES = [
        ('public', '公开房间'),
        ('private', '私有房间'),
        ('group', '群组房间'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="房间名称")
    description = models.TextField(blank=True, null=True, verbose_name="房间描述")
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='public', verbose_name="房间类型")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_rooms', verbose_name="创建者")
    members = models.ManyToManyField(User, related_name='chat_rooms', verbose_name="房间成员")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    max_members = models.IntegerField(default=50, verbose_name="最大成员数")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return f"{self.name} ({self.get_room_type_display()})"
    
    class Meta:
        db_table = 'chat_room'
        verbose_name = "聊天房间"
        verbose_name_plural = "聊天房间"
        ordering = ['-created_at']
    
    @property
    def member_count(self):
        """获取房间成员数量"""
        return self.members.count()
    
    def add_member(self, user):
        """添加成员到房间"""
        if self.member_count < self.max_members:
            self.members.add(user)
            return True
        return False
    
    def remove_member(self, user):
        """从房间移除成员"""
        self.members.remove(user)


class ChatMessage(models.Model):
    """聊天消息模型"""
    MESSAGE_TYPE_CHOICES = [
        ('text', '文本消息'),
        ('image', '图片消息'),
        ('file', '文件消息'),
        ('system', '系统消息'),
    ]
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', verbose_name="房间")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name="发送者")
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='text', verbose_name="消息类型")
    content = models.TextField(verbose_name="消息内容")
    file_url = models.URLField(blank=True, null=True, verbose_name="文件链接")
    file_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="文件名")
    file_size = models.BigIntegerField(blank=True, null=True, verbose_name="文件大小")
    is_edited = models.BooleanField(default=False, verbose_name="是否已编辑")
    is_deleted = models.BooleanField(default=False, verbose_name="是否已删除")
    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies', verbose_name="回复消息")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return f"{self.sender.username} in {self.room.name}: {self.content[:50]}"
    
    class Meta:
        db_table = 'chat_message'
        verbose_name = "聊天消息"
        verbose_name_plural = "聊天消息"
        ordering = ['-created_at']
    
    def soft_delete(self):
        """软删除消息"""
        self.is_deleted = True
        self.content = "[消息已删除]"
        self.save()


class ChatRoomMember(models.Model):
    """房间成员关系模型"""
    ROLE_CHOICES = [
        ('admin', '管理员'),
        ('moderator', '版主'),
        ('member', '普通成员'),
    ]
    
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='room_members', verbose_name="房间")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='room_memberships', verbose_name="用户")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='member', verbose_name="角色")
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="加入时间")
    last_read_at = models.DateTimeField(default=timezone.now, verbose_name="最后阅读时间")
    is_muted = models.BooleanField(default=False, verbose_name="是否静音")
    is_banned = models.BooleanField(default=False, verbose_name="是否被禁言")
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name} ({self.get_role_display()})"
    
    class Meta:
        db_table = 'chat_room_member'
        verbose_name = "房间成员"
        verbose_name_plural = "房间成员"
        unique_together = ['room', 'user']
        ordering = ['-joined_at']


class ChatMessageRead(models.Model):
    """消息已读状态模型"""
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='read_by', verbose_name="消息")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='read_messages', verbose_name="用户")
    read_at = models.DateTimeField(auto_now_add=True, verbose_name="阅读时间")
    
    def __str__(self):
        return f"{self.user.username} read message {self.message.id}"
    
    class Meta:
        db_table = 'chat_message_read'
        verbose_name = "消息已读状态"
        verbose_name_plural = "消息已读状态"
        unique_together = ['message', 'user']
        ordering = ['-read_at']


class ChatNotification(models.Model):
    """聊天通知模型"""
    NOTIFICATION_TYPE_CHOICES = [
        ('message', '新消息'),
        ('mention', '被提及'),
        ('room_invite', '房间邀请'),
        ('system', '系统通知'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_notifications', verbose_name="用户")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES, verbose_name="通知类型")
    title = models.CharField(max_length=200, verbose_name="通知标题")
    content = models.TextField(verbose_name="通知内容")
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications', verbose_name="相关房间")
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications', verbose_name="相关消息")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return f"{self.user.username}: {self.title}"
    
    class Meta:
        db_table = 'chat_notification'
        verbose_name = "聊天通知"
        verbose_name_plural = "聊天通知"
        ordering = ['-created_at']
