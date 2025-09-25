# 聊天系统安装和启动指南

## 📋 系统要求

- Python 3.10+
- MySQL 8.0+
- Redis (可选，用于生产环境)

## 🚀 快速开始

### 1. 安装依赖

```bash
# 开发环境
pip install -r requirements.txt

# 或者使用开发依赖（包含测试工具）
pip install -r requirements-dev.txt
```

### 2. 数据库配置

确保MySQL数据库已启动，并在 `myproject/settings.py` 中配置正确的数据库连接信息。

### 3. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户

```bash
python manage.py createsuperuser
```

### 5. 启动服务器

#### 方法一：使用Python启动脚本（推荐）

```bash
# 简单启动
python start_simple.py

# 完整启动脚本
python start_server.py

# 生产环境
python start_server.py --env prod
```

#### 方法二：使用批处理文件（Windows）

```bash
# 双击运行
start_chat_server.bat

# 或在PowerShell中运行
.\start_chat_server.ps1
```

#### 方法三：直接使用daphne

```bash
# 开发环境
python -m daphne -b 127.0.0.1 -p 8001 myproject.asgi:application

# 生产环境
python -m daphne -b 0.0.0.0 -p 8000 myproject.asgi:application
```

## 🔧 服务器配置

### 开发环境
- **HTTP API**: http://localhost:8000/api/chat/
- **WebSocket**: ws://localhost:8000/ws/chat/{room_id}/
- **管理后台**: http://localhost:8000/admin/

### 生产环境
- **HTTP API**: http://your-domain.com/api/chat/
- **WebSocket**: ws://your-domain.com/ws/chat/{room_id}/
- **管理后台**: http://your-domain.com/admin/

## 📡 API测试

### 1. 获取JWT Token

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### 2. 测试聊天API

```bash
# 获取房间列表
curl -X GET http://localhost:8000/api/chat/rooms/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 发送消息
curl -X POST http://localhost:8000/api/chat/rooms/1/messages/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content": "Hello World", "message_type": "text"}'
```

### 3. 测试WebSocket连接

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/1/?token=YOUR_JWT_TOKEN');

ws.onopen = function() {
    console.log('WebSocket连接已建立');
};

ws.onmessage = function(event) {
    console.log('收到消息:', event.data);
};
```

## 🛠️ 开发工具

### 代码质量检查

```bash
# 代码格式化
black .

# 导入排序
isort .

# 代码检查
flake8 .
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_chat_api.py
```

## 📚 文档

- [API接口文档](docs/chat/API_DOCUMENTATION.md)
- [使用指南](docs/chat/CHAT_GUIDE.md)
- [项目结构](docs/setup/PROJECT_STRUCTURE.md)

## 🐛 常见问题

### 1. WebSocket连接失败

**问题**: WebSocket连接返回404或500错误

**解决方案**: 
1. **端口冲突**: 检查8000端口是否被占用
2. **服务器启动**: 确保使用daphne启动服务器，而不是Django开发服务器
3. **认证问题**: WebSocket连接需要JWT认证

```bash
# 检查端口占用
netstat -ano | findstr :8000

# 终止占用进程
taskkill /f /pid <进程ID>

# 正确启动服务器
python -m daphne -b 127.0.0.1 -p 8001 myproject.asgi:application

# 或使用启动脚本
python start_simple.py
```

**注意**: WebSocket连接需要JWT认证，请确保在连接时提供有效的token：
```
ws://localhost:8001/ws/chat/{room_id}/?token=your_jwt_token
```

### 2. 依赖安装失败

**问题**: 安装某些依赖时出现错误

**解决方案**: 使用虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 数据库连接错误

**问题**: 无法连接到MySQL数据库

**解决方案**: 检查数据库配置和连接信息

## 📞 技术支持

如果遇到问题，请检查：

1. Python版本是否为3.10+
2. 所有依赖是否正确安装
3. 数据库是否正常运行
4. 防火墙设置是否允许8000端口

## 🔄 更新日志

- **v1.0.0**: 初始版本，支持基础聊天功能
- **v1.1.0**: 添加WebSocket实时通信
- **v1.2.0**: 优化权限控制和API响应
