# JWT认证API文档

## 概述

本项目提供了一套完整的基于JWT（JSON Web Token）的API认证系统，包含用户注册、登录、令牌刷新、用户档案管理等功能。

## 基础信息

- **基础URL**: `http://localhost:8000`
- **认证方式**: Bearer Token
- **令牌有效期**: 访问令牌60分钟，刷新令牌1天

## 认证流程

1. **注册** → 获取访问令牌和刷新令牌
2. **登录** → 获取访问令牌和刷新令牌
3. **使用API** → 在请求头中携带访问令牌
4. **刷新令牌** → 当访问令牌过期时，使用刷新令牌获取新的访问令牌

## API端点

### 1. 获取所有账户信息

**GET** `/api/accounts/`

**权限要求**: 需要登录认证

**请求头**:
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**响应**:
```json
{
    "success": true,
    "message": "获取所有账户信息成功",
    "data": [
        {
            "id": 1,
            "name": "张三",
            "age": 25,
            "email": "zhangsan@example.com"
        },
        {
            "id": 2,
            "name": "李四",
            "age": 30,
            "email": "lisi@example.com"
        }
    ],
    "count": 2
}
```

**错误响应** (未认证):
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 2. 用户注册

**POST** `/api/auth/register/`

**请求体**:
```json
{
    "username": "new_user",
    "email": "user@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "John",
    "last_name": "Doe"
}
```

**响应**:
```json
{
    "success": true,
    "message": "Registration successful",
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "user": {
        "id": 1,
        "username": "new_user",
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "profile": {
        "id": 1,
        "user": {...},
        "phone": null,
        "avatar": null,
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-01T00:00:00Z"
    }
}
```

### 2. 用户登录

**POST** `/api/auth/login/`

**请求体**:
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**响应**:
```json
{
    "success": true,
    "message": "Login successful",
    "tokens": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    },
    "user": {...},
    "profile": {...}
}
```

### 3. 获取用户档案

**GET** `/api/auth/profile/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应**:
```json
{
    "success": true,
    "user": {...},
    "profile": {...}
}
```

### 4. 更新用户档案

**PUT** `/api/auth/profile/update/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求体**:
```json
{
    "phone": "1234567890",
    "avatar": "https://example.com/avatar.jpg"
}
```

**响应**:
```json
{
    "success": true,
    "message": "Profile updated successfully",
    "profile": {...}
}
```

### 5. 修改密码

**POST** `/api/auth/change-password/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求体**:
```json
{
    "old_password": "old_password",
    "new_password": "new_password",
    "confirm_password": "new_password"
}
```

**响应**:
```json
{
    "success": true,
    "message": "Password changed successfully"
}
```

### 6. 刷新访问令牌

**POST** `/api/auth/refresh/`

**请求体**:
```json
{
    "refresh": "your_refresh_token"
}
```

**响应**:
```json
{
    "success": true,
    "access": "new_access_token",
    "refresh": "new_refresh_token"
}
```

### 7. 用户登出

**POST** `/api/auth/logout/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求体**:
```json
{
    "refresh_token": "your_refresh_token"
}
```

**响应**:
```json
{
    "success": true,
    "message": "Logout successful"
}
```

## 业务API

### 1. 获取账户信息

**GET** `/api/hello/`

**响应**:
```json
{
    "success": true,
    "data": [...]
}
```

### 2. 多进程处理

**POST** `/api/multiprocessing/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应**:
```json
{
    "success": true,
    "data": [结果数组]
}
```

### 3. 多线程处理

**POST** `/api/threading/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应**:
```json
{
    "success": true,
    "data": [结果数组]
}
```

### 4. Azure Blob存储


**请求头**:
```
Authorization: Bearer <access_token>
```

**请求体**:
```json
{
    "phone": "13678111111"
}
```

**响应**:
```json
{
    "success": true,
    "message": "Blob operation completed"
}
```

### 5. 数据加密

**POST** `/api/encrypt/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求体**:
```json
{
    "phone": "your_phone_number"
}
```

**响应**:
```json
{
    "success": true,
    "data": "encrypted_data"
}
```

### 6. 数据解密

**POST** `/api/decrypt/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**请求体**:
```json
{
    "asm": "encrypted_data"
}
```

**响应**:
```json
{
    "success": true,
    "data": "decrypted_data"
}
```

### 7. Pandas数据处理

**GET** `/api/panda/`

**请求头**:
```
Authorization: Bearer <access_token>
```

**响应**:
```json
{
    "success": true,
    "original_data": {...},
    "sorted_data": [...]
}
```

## 使用示例

### JavaScript/Node.js

```javascript
// 登录
const loginResponse = await fetch('/api/auth/login/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'your_username',
        password: 'your_password'
    })
});

const loginData = await loginResponse.json();
const accessToken = loginData.tokens.access;

// 使用API
const apiResponse = await fetch('/api/panda/', {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
    }
});
```

### Python

```python
import requests

# 登录
login_data = {
    'username': 'your_username',
    'password': 'your_password'
}

response = requests.post('http://localhost:8000/api/auth/login/', json=login_data)
login_result = response.json()
access_token = login_result['tokens']['access']

# 使用API
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

api_response = requests.get('http://localhost:8000/api/panda/', headers=headers)
result = api_response.json()
```

### cURL

```bash
# 登录
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'

# 使用API
curl -X GET http://localhost:8000/api/panda/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

## 错误处理

所有API都会返回统一的错误格式：

```json
{
    "success": false,
    "message": "错误描述",
    "errors": {
        "field_name": ["具体错误信息"]
    }
}
```

常见HTTP状态码：
- `200`: 成功
- `201`: 创建成功
- `400`: 请求错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器错误

## 安全注意事项

1. **令牌安全**: 不要在客户端存储刷新令牌，应该安全保存
2. **HTTPS**: 生产环境必须使用HTTPS
3. **令牌过期**: 及时刷新过期的访问令牌
4. **敏感信息**: 不要在令牌中存储敏感信息
5. **登出**: 用户登出时应该使刷新令牌失效

## 部署说明

1. 安装依赖：`pip install -r requirements.txt`
2. 运行迁移：`python manage.py migrate`
3. 创建超级用户：`python manage.py createsuperuser`
4. 启动服务器：`python manage.py runserver`

## 环境变量配置

建议将敏感信息配置为环境变量：

```python
# settings.py
import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'test'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'root'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
``` 