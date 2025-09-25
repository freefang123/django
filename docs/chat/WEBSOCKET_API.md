# WebSocket API 接口文档

## 概述

本文档描述了聊天系统的WebSocket接口，包括连接、发送和接收消息的详细参数说明。

## 连接信息

- **WebSocket地址**: `ws://localhost:8000/ws/chat/{room_id}/?token=your_jwt_token`
- **HTTP API地址**: `http://localhost:8000/api/chat/`
- **协议**: WebSocket
- **认证**: 需要JWT token认证

## 重要说明

### 消息ID说明
- **WebSocket消息ID**: 现在返回的是数据库中的真实消息ID（自增主键）
- **API调用**: 使用WebSocket返回的消息ID调用HTTP API
- **示例**: 如果WebSocket返回 `{"id": 123}`，则调用 `POST http://localhost:8000/api/chat/messages/123/read/`

## 连接参数

### URL参数
- `room_id`: 聊天房间ID（必需）
  - 类型: 整数
  - 示例: `ws://localhost:8001/ws/chat/2/`

## 发送消息格式

### 1. 聊天消息

```json
{
  "type": "chat_message",
  "content": "消息内容",
  "message_type": "text"
}
```

**参数说明:**
- `type` (string, 必需): 消息类型，固定为 "chat_message"
- `content` (string, 必需): 消息内容
- `message_type` (string, 可选): 消息类型，默认为 "text"
  - 可选值: "text", "image", "file", "system"

### 2. 正在输入状态

```json
{
  "type": "typing",
  "is_typing": true
}
```

**参数说明:**
- `type` (string, 必需): 消息类型，固定为 "typing"
- `is_typing` (boolean, 必需): 是否正在输入

### 3. 用户加入

```json
{
  "type": "user_join"
}
```

**参数说明:**
- `type` (string, 必需): 消息类型，固定为 "user_join"

### 4. 用户离开

```json
{
  "type": "user_leave"
}
```

**参数说明:**
- `type` (string, 必需): 消息类型，固定为 "user_leave"

## 接收消息格式

### 1. 连接确认

```json
{
  "type": "connection_established",
  "message": "连接成功",
  "user": {
    "id": 1,
    "username": "real_user"
  }
}
```

**参数说明:**
- `type` (string): 消息类型，固定为 "connection_established"
- `message` (string): 确认消息
- `user` (object): 用户信息
  - `id` (number): 用户ID
  - `username` (string): 用户名

### 2. 聊天消息

```json
{
  "type": "chat_message",
  "message": {
    "id": 1758787632222,
    "content": "消息内容",
    "message_type": "text",
    "timestamp": "2025-01-25T15:30:00Z",
    "sender": {
      "id": 1,
      "username": "anonymous"
    }
  }
}
```

**参数说明:**
- `type` (string): 消息类型，固定为 "chat_message"
- `message` (object): 消息对象
  - `id` (integer): 消息唯一ID（时间戳，如：1758787632222）
  - `content` (string): 消息内容
  - `message_type` (string): 消息类型
  - `timestamp` (string): 时间戳
  - `sender` (object): 发送者信息
    - `id` (integer): 用户ID（如果未认证，默认为1）
    - `username` (string): 用户名（如果未认证，默认为"anonymous"）

### 3. 正在输入状态

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

**参数说明:**
- `type` (string): 消息类型，固定为 "typing"
- `user` (object): 用户信息
  - `id` (integer): 用户ID
  - `username` (string): 用户名
- `is_typing` (boolean): 是否正在输入

### 4. 用户加入

```json
{
  "type": "user_join",
  "user": {
    "id": 1,
    "username": "user"
  }
}
```

**参数说明:**
- `type` (string): 消息类型，固定为 "user_join"
- `user` (object): 用户信息
  - `id` (integer): 用户ID
  - `username` (string): 用户名

### 5. 用户离开

```json
{
  "type": "user_leave",
  "user": {
    "id": 1,
    "username": "user"
  }
}
```

**参数说明:**
- `type` (string): 消息类型，固定为 "user_leave"
- `user` (object): 用户信息
  - `id` (integer): 用户ID
  - `username` (string): 用户名

### 6. 错误消息

```json
{
  "type": "error",
  "message": "错误信息"
}
```

**参数说明:**
- `type` (string): 消息类型，固定为 "error"
- `message` (string): 错误信息

## 使用示例

### JavaScript 客户端示例

```javascript
// 获取JWT token（从localStorage或其他地方）
const token = localStorage.getItem('jwt_token');

// 连接WebSocket（带认证）
const ws = new WebSocket(`ws://localhost:8000/ws/chat/2/?token=${token}`);

// 连接成功
ws.onopen = function(event) {
    console.log('WebSocket连接成功');
};

// 接收消息
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'connection_established':
            console.log('连接确认:', data.message);
            break;
            
        case 'chat_message':
            console.log('收到消息:', data.message);
            console.log('消息ID:', data.message.id);
            console.log('消息内容:', data.message.content);
            break;
            
        case 'typing':
            console.log('用户正在输入:', data.user.username, data.is_typing);
            break;
            
        case 'user_join':
            console.log('用户加入:', data.user.username);
            break;
            
        case 'user_leave':
            console.log('用户离开:', data.user.username);
            break;
            
        case 'error':
            console.error('错误:', data.message);
            break;
    }
};

// 发送聊天消息
function sendMessage(content) {
    const message = {
        type: 'chat_message',
        content: content,
        message_type: 'text'
    };
    ws.send(JSON.stringify(message));
}

// 发送正在输入状态
function sendTyping(isTyping) {
    const message = {
        type: 'typing',
        is_typing: isTyping
    };
    ws.send(JSON.stringify(message));
}

// 关闭连接
ws.onclose = function(event) {
    console.log('WebSocket连接关闭');
};
```

### Python 客户端示例

```python
import asyncio
import websockets
import json

async def chat_client():
    # 获取JWT token
    token = "your_jwt_token_here"
    uri = f"ws://localhost:8000/ws/chat/2/?token={token}"
    
    async with websockets.connect(uri) as websocket:
        print("WebSocket连接成功")
        
        # 发送聊天消息
        message = {
            "type": "chat_message",
            "content": "Hello WebSocket!",
            "message_type": "text"
        }
        await websocket.send(json.dumps(message))
        
        # 接收消息
        response = await websocket.recv()
        data = json.loads(response)
        print(f"收到消息: {data}")

# 运行客户端
asyncio.run(chat_client())
```

## 错误处理

### 常见错误

1. **连接失败**
   - 检查WebSocket地址是否正确
   - 确认服务器是否正在运行
   - 检查网络连接

2. **消息格式错误**
   - 确保JSON格式正确
   - 检查必需字段是否存在
   - 验证数据类型是否正确

3. **房间不存在**
   - 确认房间ID是否正确
   - 检查房间是否已创建

## 注意事项

1. **消息ID**: 每条消息都有唯一的ID，基于时间戳生成
2. **消息类型**: 支持文本、图片、文件、系统消息等类型
3. **实时性**: WebSocket提供实时双向通信
4. **错误处理**: 建议实现完整的错误处理机制
5. **连接管理**: 需要处理连接断开和重连逻辑

## 更新日志

- **v1.0.0**: 初始版本，支持基本的聊天功能
- **v1.1.0**: 添加消息ID支持
- **v1.2.0**: 更新端口为8001
