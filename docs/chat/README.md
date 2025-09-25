# 聊天系统文档

## 概述

这是一个基于Django的完整聊天系统，支持房间会话、实时消息传递、消息历史记录等功能。系统采用REST API + WebSocket的架构，专为React前端项目设计。

## 核心特性

- ✅ **权限控制**：任何已登录的用户都可以访问
- ✅ **房间管理**：创建、加入、离开房间
- ✅ **实时通信**：WebSocket实时消息传递
- ✅ **消息历史**：完整的消息记录和查询
- ✅ **通知系统**：消息通知和已读状态
- ✅ **JWT认证**：安全的用户认证机制

## 技术架构

### 后端技术栈
- **Django 5.2.4** - Web框架
- **Django REST Framework** - API框架
- **Django Channels** - WebSocket支持
- **MySQL** - 数据库
- **JWT认证** - 用户认证

### 前端集成
- **React** - 前端框架（由外部项目提供）
- **WebSocket API** - 实时通信
- **REST API** - 数据交互

## 快速开始

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

## 文档结构

```
docs/chat/
├── README.md                    # 本文档
├── API_DOCUMENTATION.md        # 完整API接口文档
└── CHAT_GUIDE.md              # 详细使用指南
```

## API接口概览

### 认证接口
- `POST /api/token/` - 获取JWT token
- `POST /api/token/refresh/` - 刷新token

### 房间管理
- `GET /api/chat/rooms/` - 获取房间列表
- `POST /api/chat/rooms/` - 创建房间
- `GET /api/chat/rooms/{id}/` - 获取房间详情
- `POST /api/chat/rooms/{room_id}/join/` - 加入房间
- `POST /api/chat/rooms/{room_id}/leave/` - 离开房间
- `GET /api/chat/rooms/{room_id}/members/` - 获取房间成员

### 消息管理
- `GET /api/chat/rooms/{room_id}/messages/` - 获取房间消息
- `POST /api/chat/rooms/{room_id}/messages/` - 发送消息
- `POST /api/chat/messages/{message_id}/read/` - 标记消息已读
- `DELETE /api/chat/messages/{message_id}/delete/` - 删除消息

### 通知管理
- `GET /api/chat/notifications/` - 获取通知列表
- `POST /api/chat/notifications/{notification_id}/read/` - 标记通知已读

### WebSocket
- `ws://localhost:8000/ws/chat/{room_id}/` - 实时通信连接

## 测试

### 测试账户
- 用户名：`developer`
- 密码：`developer123`

### API测试页面
访问 `http://localhost:8000/api/chat/test/` 查看API接口文档和测试页面。

## 数据模型

### 核心模型
- **ChatRoom** - 聊天房间
- **ChatMessage** - 聊天消息
- **ChatRoomMember** - 房间成员关系
- **ChatNotification** - 通知系统
- **ChatMessageRead** - 消息已读状态

## 权限控制

系统采用简单的认证控制：
- 任何已登录的用户都可以访问聊天功能
- 所有API接口都需要JWT认证
- WebSocket连接也会验证用户认证状态

## 部署注意事项

1. **Redis配置**：生产环境需要配置Redis作为WebSocket后端
2. **静态文件**：确保静态文件正确配置
3. **CORS设置**：配置正确的CORS设置
4. **HTTPS**：生产环境建议使用HTTPS
5. **负载均衡**：多服务器部署需要配置WebSocket负载均衡

## 扩展功能

可以进一步扩展的功能：
- 文件上传和分享
- 表情符号支持
- 消息搜索
- 私聊功能
- 消息加密
- 语音/视频通话
- 机器人集成

## 支持

如有问题，请参考：
1. `docs/chat/API_DOCUMENTATION.md` - 完整API文档
2. `docs/chat/CHAT_GUIDE.md` - 详细使用指南
3. API测试页面：`http://localhost:8000/api/chat/test/`
