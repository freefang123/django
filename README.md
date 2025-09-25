# Django JWT认证API系统

## 项目概述

这是一个基于Django REST Framework和JWT（JSON Web Token）的完整API认证系统，提供了用户注册、登录、令牌管理、用户档案管理等功能，同时集成了多种业务功能如多进程处理、数据加密、Azure云存储等。

## 功能特性

### 🔐 认证系统
- **JWT认证**: 基于JWT的无状态认证
- **用户注册**: 完整的用户注册流程
- **用户登录**: 安全的用户登录机制
- **令牌刷新**: 自动刷新过期的访问令牌
- **用户登出**: 安全的登出机制
- **用户档案**: 用户档案管理功能
- **密码修改**: 安全的密码修改功能

### 🚀 业务功能
- **多进程处理**: 并发计算斐波那契数列
- **多线程处理**: 并发数据处理
- **数据加密/解密**: AES加密算法
- **Azure Blob存储**: 云存储集成
- **Pandas数据处理**: 数据分析和处理
- **数据库操作**: MySQL数据库集成

## 技术栈

- **后端框架**: Django 5.2.4
- **API框架**: Django REST Framework 3.16.0
- **JWT认证**: djangorestframework-simplejwt 5.5.1
- **数据库**: MySQL
- **数据处理**: Pandas, NumPy
- **云服务**: Azure Storage Blob
- **加密**: PyCryptodome, Cryptography

## 项目结构

```
myproject/
├── manage.py                 # Django管理脚本
├── requirements.txt          # 项目依赖
├── README.md               # 项目说明
├── API_DOCUMENTATION.md    # API文档
├── test_api.py             # API测试脚本
├── myproject/              # 主项目配置
│   ├── settings.py         # Django设置
│   ├── urls.py            # 主URL配置
│   ├── wsgi.py            # WSGI配置
│   └── asgi.py            # ASGI配置
├── myapp/                  # 主应用
│   ├── models.py          # 数据模型
│   ├── serializers.py     # 序列化器
│   ├── views.py           # 原始视图
│   ├── auth_views.py      # 认证视图
│   ├── api_views.py       # API视图
│   ├── utils.py           # 工具函数
│   ├── urls.py            # 应用URL配置
│   ├── api_urls.py        # API URL配置
│   ├── auth_urls.py       # 认证URL配置
│   └── migrations/        # 数据库迁移
├── templates/              # 模板文件
│   └── index.html
└── static/                # 静态文件
```

## 快速开始

### 1. 环境准备

确保已安装Python 3.8+和MySQL数据库。

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 数据库配置

在`myproject/settings.py`中配置数据库连接：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 4. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. 创建超级用户

```bash
python manage.py createsuperuser
```

### 6. 启动服务器

```bash
python manage.py runserver
```

### 7. 测试API

```bash
python test_api.py
```

## API端点

### 认证相关

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/api/auth/register/` | 用户注册 |
| POST | `/api/auth/login/` | 用户登录 |
| GET | `/api/auth/profile/` | 获取用户档案 |
| PUT | `/api/auth/profile/update/` | 更新用户档案 |
| POST | `/api/auth/change-password/` | 修改密码 |
| POST | `/api/auth/refresh/` | 刷新令牌 |
| POST | `/api/auth/logout/` | 用户登出 |

### 业务功能

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/api/hello/` | 获取账户信息 |
| POST | `/api/multiprocessing/` | 多进程处理 |
| POST | `/api/threading/` | 多线程处理 |
| POST | `/api/blob/` | Azure Blob存储 |
| GET | `/api/blob-url/` | 获取Blob链接 |
| POST | `/api/encrypt/` | 数据加密 |
| POST | `/api/decrypt/` | 数据解密 |
| GET | `/api/panda/` | Pandas数据处理 |

## 使用示例

### 用户注册

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### 用户登录

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### 使用API

```bash
curl -X GET http://localhost:8000/api/panda/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json"
```

## 配置说明

### JWT配置

在`settings.py`中配置JWT相关设置：

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 安全配置

建议在生产环境中：

1. 启用CSRF保护
2. 使用HTTPS
3. 配置环境变量
4. 设置DEBUG=False
5. 配置ALLOWED_HOSTS

## 开发指南

### 添加新的API端点

1. 在`myapp/api_views.py`中添加视图函数
2. 在`myapp/api_urls.py`中添加URL路由
3. 添加相应的序列化器（如需要）
4. 编写测试用例

### 自定义认证

可以扩展JWT认证类来实现自定义认证逻辑：

```python
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # 自定义认证逻辑
        pass
```

## 部署

### 生产环境配置

1. 设置环境变量
2. 配置数据库连接
3. 配置静态文件
4. 使用Gunicorn或uWSGI
5. 配置Nginx反向代理

### Docker部署

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 测试

运行测试脚本：

```bash
python test_api.py
```

或者使用Django测试框架：

```bash
python manage.py test
```

## 贡献

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交Issue或联系开发者。

---

**注意**: 这是一个开发环境的配置，生产环境请务必修改安全设置和敏感信息。 