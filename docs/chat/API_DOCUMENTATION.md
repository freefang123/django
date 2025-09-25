# 聊天系统 API 接口文档

## 概述

本文档描述了聊天系统的所有API接口，供React前端项目使用。所有接口都需要JWT认证，任何已登录的用户都可以访问聊天功能。

## 基础信息

- **Base URL**: `http://localhost:8000/api/chat/`
- **WebSocket URL**: `ws://localhost:8000/ws/chat/{room_id}/`
- **认证方式**: JWT Bearer Token
- **权限要求**: 任何已登录的用户都可以访问
- **数据格式**: JSON

## 服务器启动

### 开发环境
```bash
# 安装依赖
pip install -r requirements.txt

# 启动ASGI服务器（支持WebSocket）
daphne -b 127.0.0.1 -p 8000 myproject.asgi:application
```

### 生产环境
```bash
# 安装生产依赖
pip install -r requirements-prod.txt

# 使用daphne启动
daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
```

## WebSocket 接口

### 连接信息
- **地址**: `ws://localhost:8000/ws/chat/{room_id}/`
- **协议**: WebSocket
- **认证**: 当前版本无需认证（简化版本）

### 发送消息格式

#### 1. 聊天消息
```json
{
  "type": "chat_message",
  "content": "消息内容",
  "message_type": "text"
}
```

#### 2. 正在输入状态
```json
{
  "type": "typing",
  "is_typing": true
}
```

### 接收消息格式

#### 1. 连接确认
```json
{
  "type": "connection_established",
  "message": "连接成功"
}
```

#### 2. 聊天消息
```json
{
  "type": "chat_message",
  "message": {
    "id": 1735123456789,
    "content": "消息内容",
    "message_type": "text",
    "timestamp": "2025-01-25T15:30:00Z",
    "sender": {
      "id": 1,
      "username": "user"
    }
  }
}
```

#### 3. 正在输入状态
```json
{
  "type": "typing",
  "user": {
    "id": 1,
    "username": "user"
  },
  "is_typing": true
}
```

#### 4. 用户加入/离开
```json
{
  "type": "user_join",
  "user": {
    "id": 1,
    "username": "user"
  }
}
```

#### 5. 错误消息
```json
{
  "type": "error",
  "message": "错误信息"
}
```

> **注意**: 详细的WebSocket接口文档请参考 [WEBSOCKET_API.md](WEBSOCKET_API.md)

## 认证

所有API请求都需要在请求头中包含JWT token：

```http
Authorization: Bearer <your_jwt_token>
Content-Type: application/json
```

## 错误响应格式

```json
{
    "error": "错误描述信息"
}
```

## API 接口列表

### 1. 房间管理

#### 1.1 获取房间列表
```http
GET /api/chat/rooms/
```

**响应示例**:
```json
[
    {
        "id": 1,
        "name": "开发讨论",
        "description": "开发团队讨论群",
        "room_type": "public",
        "created_by": {
            "id": 1,
            "username": "developer",
            "first_name": "Developer",
            "last_name": "User"
        },
        "member_count": 5,
        "last_message": {
            "id": 10,
            "content": "大家好！",
            "sender": "developer",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "created_at": "2024-01-01T10:00:00Z"
    }
]
```

#### 1.2 创建房间
```http
POST /api/chat/rooms/
```

**请求体**:
```json
{
    "name": "新房间",
    "description": "房间描述",
    "room_type": "public",
    "max_members": 50
}
```

**参数说明**:
- `name` (string, 必填): 房间名称
- `description` (string, 可选): 房间描述
- `room_type` (string, 必填): 房间类型，可选值: `public`, `private`, `group`
- `max_members` (integer, 可选): 最大成员数，默认50

**响应示例**:
```json
{
    "id": 2,
    "name": "新房间",
    "description": "房间描述",
    "room_type": "public",
    "created_by": {
        "id": 1,
        "username": "developer"
    },
    "member_count": 1,
    "is_active": true,
    "max_members": 50,
    "created_at": "2024-01-01T12:00:00Z"
}
```

#### 1.3 获取房间详情
```http
GET /api/chat/rooms/{room_id}/
```

**响应示例**:
```json
{
    "id": 1,
    "name": "开发讨论",
    "description": "开发团队讨论群",
    "room_type": "public",
    "created_by": {
        "id": 1,
        "username": "developer",
        "first_name": "Developer",
        "last_name": "User"
    },
    "members": [
        {
            "id": 1,
            "username": "developer",
            "first_name": "Developer",
            "last_name": "User"
        }
    ],
    "member_count": 1,
    "is_active": true,
    "max_members": 50,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}
```

#### 1.4 加入房间
```http
POST /api/chat/rooms/{room_id}/join/
```

**响应示例**:
```json
{
    "message": "成功加入房间"
}
```

#### 1.5 离开房间
```http
POST /api/chat/rooms/{room_id}/leave/
```

**响应示例**:
```json
{
    "message": "成功离开房间"
}
```

#### 1.6 获取房间成员
```http
GET /api/chat/rooms/{room_id}/members/
```

**响应示例**:
```json
[
    {
        "id": 1,
        "room": {
            "id": 1,
            "name": "开发讨论"
        },
        "user": {
            "id": 1,
            "username": "developer",
            "first_name": "Developer",
            "last_name": "User"
        },
        "role": "admin",
        "joined_at": "2024-01-01T10:00:00Z",
        "last_read_at": "2024-01-01T12:00:00Z",
        "is_muted": false,
        "is_banned": false
    }
]
```

### 2. 消息管理

#### 2.1 获取房间消息
```http
GET /api/chat/rooms/{room_id}/messages/
```

**查询参数**:
- `page` (integer, 可选): 页码，默认1
- `page_size` (integer, 可选): 每页数量，默认20

**响应示例**:
```json
{
    "messages": [
        {
            "id": 1,
            "room": {
                "id": 1,
                "name": "开发讨论"
            },
            "sender": {
                "id": 1,
                "username": "developer",
                "first_name": "Developer",
                "last_name": "User"
            },
            "message_type": "text",
            "content": "大家好！",
            "file_url": null,
            "file_name": null,
            "file_size": null,
            "is_edited": false,
            "is_deleted": false,
            "reply_to": null,
            "created_at": "2024-01-01T12:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        }
    ],
    "page": 1,
    "page_size": 20,
    "total": 1
}
```

#### 2.2 发送消息
```http
POST /api/chat/rooms/{room_id}/messages/
```

**请求体**:
```json
{
    "content": "消息内容",
    "message_type": "text",
    "file_url": "https://example.com/file.jpg",
    "file_name": "image.jpg",
    "file_size": 1024,
    "reply_to": 1
}
```

**参数说明**:
- `content` (string, 必填): 消息内容
- `message_type` (string, 可选): 消息类型，可选值: `text`, `image`, `file`, `system`，默认`text`
- `file_url` (string, 可选): 文件链接
- `file_name` (string, 可选): 文件名
- `file_size` (integer, 可选): 文件大小（字节）
- `reply_to` (integer, 可选): 回复的消息ID

**响应示例**:
```json
{
    "id": 2,
    "room": {
        "id": 1,
        "name": "开发讨论"
    },
    "sender": {
        "id": 1,
        "username": "developer",
        "first_name": "Developer",
        "last_name": "User"
    },
    "message_type": "text",
    "content": "消息内容",
    "file_url": null,
    "file_name": null,
    "file_size": null,
    "is_edited": false,
    "is_deleted": false,
    "reply_to": null,
    "created_at": "2024-01-01T12:05:00Z",
    "updated_at": "2024-01-01T12:05:00Z"
}
```

#### 2.3 标记消息已读
```http
POST /api/chat/messages/{message_id}/read/
```

**响应示例**:
```json
{
    "message": "消息已标记为已读"
}
```

#### 2.4 删除消息
```http
DELETE /api/chat/messages/{message_id}/delete/
```

**响应示例**:
```json
{
    "message": "消息已删除"
}
```

### 3. 通知管理

#### 3.1 获取通知列表
```http
GET /api/chat/notifications/
```

**响应示例**:
```json
[
    {
        "id": 1,
        "notification_type": "message",
        "title": "新消息来自 developer",
        "content": "大家好！",
        "room": {
            "id": 1,
            "name": "开发讨论",
            "description": "开发团队讨论群",
            "room_type": "public",
            "created_by": {
                "id": 1,
                "username": "developer"
            },
            "member_count": 5,
            "is_active": true,
            "max_members": 50,
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-01T12:00:00Z"
        },
        "message": {
            "id": 1,
            "content": "大家好！",
            "message_type": "text",
            "created_at": "2024-01-01T12:00:00Z"
        },
        "is_read": false,
        "created_at": "2024-01-01T12:00:00Z"
    }
]
```

#### 3.2 标记通知已读
```http
POST /api/chat/notifications/{notification_id}/read/
```

**响应示例**:
```json
{
    "message": "通知已标记为已读"
}
```

## WebSocket 接口

### 连接地址
```
ws://localhost:8000/ws/chat/{room_id}/
```

### 认证
WebSocket连接需要在URL中包含JWT token或通过其他方式认证。

### 消息格式

#### 发送消息格式

**发送聊天消息**:
```json
{
    "type": "chat_message",
    "content": "消息内容",
    "message_type": "text",
    "reply_to": 1
}
```

**发送正在输入状态**:
```json
{
    "type": "typing",
    "is_typing": true
}
```

**用户加入通知**:
```json
{
    "type": "user_join"
}
```

**用户离开通知**:
```json
{
    "type": "user_leave"
}
```

#### 接收消息格式

**接收聊天消息**:
```json
{
    "type": "chat_message",
    "message": {
        "id": 1,
        "sender": {
            "id": 1,
            "username": "developer",
            "first_name": "Developer",
            "last_name": "User"
        },
        "content": "消息内容",
        "message_type": "text",
        "created_at": "2024-01-01T12:00:00Z",
        "reply_to": null
    }
}
```

**接收正在输入状态**:
```json
{
    "type": "typing",
    "user": {
        "id": 1,
        "username": "developer"
    },
    "is_typing": true
}
```

**接收用户加入通知**:
```json
{
    "type": "user_join",
    "user": {
        "id": 1,
        "username": "developer"
    }
}
```

**接收用户离开通知**:
```json
{
    "type": "user_leave",
    "user": {
        "id": 1,
        "username": "developer"
    }
}
```

**连接建立确认**:
```json
{
    "type": "connection_established",
    "message": "连接成功"
}
```

**错误消息**:
```json
{
    "type": "error",
    "message": "错误描述"
}
```

## 数据模型说明

### ChatRoom（聊天房间）
- `id`: 房间ID
- `name`: 房间名称
- `description`: 房间描述
- `room_type`: 房间类型（public/private/group）
- `created_by`: 创建者信息
- `members`: 房间成员列表
- `member_count`: 成员数量
- `is_active`: 是否激活
- `max_members`: 最大成员数
- `created_at`: 创建时间
- `updated_at`: 更新时间

### ChatMessage（聊天消息）
- `id`: 消息ID
- `room`: 所属房间
- `sender`: 发送者
- `message_type`: 消息类型（text/image/file/system）
- `content`: 消息内容
- `file_url`: 文件链接
- `file_name`: 文件名
- `file_size`: 文件大小
- `is_edited`: 是否已编辑
- `is_deleted`: 是否已删除
- `reply_to`: 回复的消息ID
- `created_at`: 创建时间
- `updated_at`: 更新时间

### ChatNotification（通知）
- `id`: 通知ID
- `notification_type`: 通知类型（message/mention/room_invite/system）
- `title`: 通知标题
- `content`: 通知内容
- `room`: 相关房间
- `message`: 相关消息
- `is_read`: 是否已读
- `created_at`: 创建时间

## 错误码说明

| HTTP状态码 | 说明 |
|-----------|------|
| 200 | 请求成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 权限不足 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

## 使用示例

### JavaScript/React 示例

```javascript
// 获取JWT token
const token = localStorage.getItem('access_token');

// 获取房间列表
const getRooms = async () => {
    const response = await fetch('/api/chat/rooms/', {
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        }
    });
    return await response.json();
};

// 创建房间
const createRoom = async (roomData) => {
    const response = await fetch('/api/chat/rooms/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(roomData)
    });
    return await response.json();
};

// 发送消息
const sendMessage = async (roomId, messageData) => {
    const response = await fetch(`/api/chat/rooms/${roomId}/messages/`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(messageData)
    });
    return await response.json();
};

// WebSocket连接
const connectWebSocket = (roomId) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/`);
    
    ws.onopen = () => {
        console.log('WebSocket连接已建立');
    };
    
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        console.log('收到消息:', data);
    };
    
    ws.onclose = () => {
        console.log('WebSocket连接已关闭');
    };
    
    return ws;
};

// 发送WebSocket消息
const sendWebSocketMessage = (ws, content) => {
    ws.send(JSON.stringify({
        type: 'chat_message',
        content: content,
        message_type: 'text'
    }));
};
```

## 注意事项

1. **权限控制**: 所有接口都需要`developer`角色权限
2. **JWT认证**: 所有请求都需要有效的JWT token
3. **WebSocket认证**: WebSocket连接也需要权限验证
4. **错误处理**: 请妥善处理各种错误情况
5. **分页**: 消息列表支持分页，建议合理设置页面大小
6. **实时性**: 使用WebSocket实现实时通信，REST API用于历史数据
7. **文件上传**: 文件消息需要先上传文件获取URL，然后发送消息
8. **消息删除**: 消息删除是软删除，内容会被替换为"[消息已删除]"
