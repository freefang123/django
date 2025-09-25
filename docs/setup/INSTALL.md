# 安装说明

## 环境要求

- Python 3.8+
- MySQL 5.7+ 或 8.0+
- pip 20.0+

## 安装步骤

### 1. 创建虚拟环境（推荐）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖

#### 基础安装（推荐用于开发）

```bash
pip install -r requirements.txt
```

#### 开发环境安装（包含开发工具）

```bash
pip install -r requirements-dev.txt
```

#### 生产环境安装（最小依赖）

```bash
pip install -r requirements-prod.txt
```

### 3. 数据库配置

确保MySQL服务正在运行，并创建数据库：

```sql
CREATE DATABASE myproject CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 环境变量配置

创建 `.env` 文件（可选）：

```bash
# 数据库配置
DB_NAME=myproject
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306

# Django配置
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Azure配置
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_STORAGE_ACCOUNT_NAME=your-account-name
AZURE_STORAGE_ACCOUNT_KEY=your-account-key
```

### 5. 数据库迁移

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. 创建超级用户

```bash
python manage.py createsuperuser
```

### 7. 启动服务器

```bash
python manage.py runserver
```

## 依赖说明

### 核心依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| Django | 5.2.4 | Web框架 |
| djangorestframework | 3.16.0 | API框架 |
| djangorestframework-simplejwt | 5.5.1 | JWT认证 |
| mysqlclient | 2.2.7 | MySQL数据库驱动 |
| pandas | 2.2.2 | 数据处理 |
| cryptography | 43.0.3 | 加密功能 |

### 可选依赖

#### 开发工具
- `pytest`: 测试框架
- `black`: 代码格式化
- `flake8`: 代码检查
- `django-debug-toolbar`: 调试工具

#### 生产工具
- `gunicorn`: WSGI服务器
- `whitenoise`: 静态文件服务

## 常见问题

### 1. MySQL连接错误

确保MySQL服务正在运行，并检查连接配置：

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}
```

### 2. 依赖安装失败

如果某些包安装失败，可以尝试：

```bash
# 升级pip
python -m pip install --upgrade pip

# 安装编译工具（Windows）
# 下载并安装 Visual Studio Build Tools

# 使用预编译包
pip install --only-binary=all package_name
```

### 3. 虚拟环境问题

如果虚拟环境有问题，可以重新创建：

```bash
# 删除旧环境
rm -rf venv

# 重新创建
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows
```

## 验证安装

运行测试脚本验证安装：

```bash
python test_api.py
```

如果看到成功的API响应，说明安装正确。

## 生产部署

### 使用Gunicorn

```bash
pip install gunicorn
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000
```

### 使用Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements-prod.txt .
RUN pip install -r requirements-prod.txt

COPY . .
RUN python manage.py collectstatic --noinput

EXPOSE 8000
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 更新依赖

定期更新依赖以获取安全补丁：

```bash
# 查看过期的包
pip list --outdated

# 更新特定包
pip install --upgrade package_name

# 更新所有包（谨慎使用）
pip install --upgrade -r requirements.txt
```

## 安全建议

1. 定期更新依赖包
2. 使用虚拟环境隔离项目
3. 不要在代码中硬编码敏感信息
4. 生产环境使用HTTPS
5. 配置适当的防火墙规则 