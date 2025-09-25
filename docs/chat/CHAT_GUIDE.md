# 在线聊天功能使用指南

## 功能概述

本系统实现了完整的在线聊天功能，支持：
- 房间会话管理
- 实时消息传递（WebSocket）
- 消息历史记录
- 权限控制（仅developer角色可访问）
- 响应式前端界面

## 技术架构

### 后端技术栈
- **Django 5.2.4** - Web框架
- **Django REST Framework** - API框架
- **Django Channels** - WebSocket支持
- **MySQL** - 数据库
- **JWT认证** - 用户认证

### 前端技术栈
- **React** - 前端框架（由外部项目提供）
- **WebSocket API** - 实时通信
- **REST API** - 数据交互

## 功能特性

### 1. 权限控制
- 只有`developer`角色的用户才能访问聊天功能
- 所有API接口都有权限验证
- WebSocket连接也会验证用户权限

### 2. 房间管理
- 创建聊天房间
- 加入/离开房间
- 房间成员管理
- 房间类型：公开、私有、群组

### 3. 实时通信
- WebSocket实时消息传递
- 正在输入状态显示
- 用户加入/离开通知
- 消息已读状态

### 4. 消息功能
- 发送文本消息
- 消息历史记录
- 消息软删除
- 回复消息功能

## 安装和配置

### 1. 安装依赖
```bash
pip install channels channels-redis
```

### 2. 数据库迁移
```bash
python manage.py makemigrations chat_app
python manage.py migrate
```

### 3. 创建developer用户组
```bash
python create_developer_group.py
```

### 4. 启动服务器
```bash
python manage.py runserver
```

## API接口文档

### 认证
所有API都需要JWT认证，在请求头中包含：
```
Authorization: Bearer <your_jwt_token>
```

### 房间相关接口

#### 获取房间列表
```
GET /api/chat/rooms/
```

#### 创建房间
```
POST /api/chat/rooms/
Content-Type: application/json

{
    "name": "房间名称",
    "description": "房间描述",
    "room_type": "public|private|group"
}
```

#### 加入房间
```
POST /api/chat/rooms/{room_id}/join/
```

#### 离开房间
```
POST /api/chat/rooms/{room_id}/leave/
```

#### 获取房间消息
```
GET /api/chat/rooms/{room_id}/messages/
```

### 消息相关接口

#### 发送消息
```
POST /api/chat/rooms/{room_id}/messages/
Content-Type: application/json

{
    "content": "消息内容",
    "message_type": "text"
}
```

#### 标记消息已读
```
POST /api/chat/messages/{message_id}/read/
```

#### 删除消息
```
DELETE /api/chat/messages/{message_id}/delete/
```

### 通知相关接口

#### 获取通知
```
GET /api/chat/notifications/
```

#### 标记通知已读
```
POST /api/chat/notifications/{notification_id}/read/
```

## WebSocket连接

### 连接地址
```
ws://localhost:8000/ws/chat/{room_id}/
```

### 消息格式

#### 发送消息
```json
{
    "type": "chat_message",
    "content": "消息内容",
    "message_type": "text"
}
```

#### 正在输入状态
```json
{
    "type": "typing",
    "is_typing": true
}
```

#### 接收消息
```json
{
    "type": "chat_message",
    "message": {
        "id": 1,
        "sender": {
            "id": 1,
            "username": "developer"
        },
        "content": "消息内容",
        "created_at": "2024-01-01T12:00:00Z"
    }
}
```

## React前端集成

### 1. API集成
请参考 `docs/chat/API_DOCUMENTATION.md` 获取完整的API接口文档。

### 2. 认证
使用JWT token进行认证：
```javascript
const token = localStorage.getItem('access_token');
```

### 3. 主要功能
1. **房间管理**：创建、加入、离开房间
2. **消息发送**：通过REST API发送消息
3. **实时通信**：使用WebSocket接收实时消息
4. **通知系统**：获取和处理通知

### 4. 示例代码
详细的JavaScript/React示例代码请参考API文档。

## 数据库模型

### ChatRoom（聊天房间）
- `name` - 房间名称
- `description` - 房间描述
- `room_type` - 房间类型
- `created_by` - 创建者
- `members` - 房间成员
- `is_active` - 是否激活

### ChatMessage（聊天消息）
- `room` - 所属房间
- `sender` - 发送者
- `content` - 消息内容
- `message_type` - 消息类型
- `is_deleted` - 是否已删除

### ChatRoomMember（房间成员）
- `room` - 房间
- `user` - 用户
- `role` - 角色（admin/moderator/member）

### ChatNotification（通知）
- `user` - 用户
- `notification_type` - 通知类型
- `title` - 通知标题
- `content` - 通知内容

## 安全考虑

1. **权限验证**：所有接口都验证用户权限
2. **JWT认证**：使用JWT token进行身份验证
3. **WebSocket安全**：WebSocket连接也验证用户权限
4. **数据验证**：所有输入数据都进行验证
5. **SQL注入防护**：使用Django ORM防止SQL注入

## 部署注意事项

1. **Redis配置**：生产环境需要配置Redis作为WebSocket后端
2. **静态文件**：确保静态文件正确配置
3. **CORS设置**：配置正确的CORS设置
4. **HTTPS**：生产环境建议使用HTTPS
5. **负载均衡**：多服务器部署需要配置WebSocket负载均衡

## 故障排除

### 常见问题

1. **WebSocket连接失败**
   - 检查channels配置
   - 确认ASGI配置正确

2. **权限错误**
   - 确认用户已添加到developer组
   - 检查JWT token是否有效

3. **消息发送失败**
   - 检查用户是否在房间中
   - 确认房间状态正常

4. **前端显示异常**
   - 检查浏览器控制台错误
   - 确认静态文件加载正常

## 扩展功能

可以进一步扩展的功能：
- 文件上传和分享
- 表情符号支持
- 消息搜索
- 私聊功能
- 消息加密
- 语音/视频通话
- 机器人集成
