# 安全配置指南

## 环境变量配置

### 1. 创建环境变量文件
```bash
# 复制示例文件
cp .env.example .env

# 编辑环境变量
nano .env
```

### 2. 必需的环境变量

#### Django 基础配置
```bash
SECRET_KEY=your-very-secret-key-here
DEBUG=False  # 生产环境必须设为 False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

#### 数据库配置
```bash
# SQLite (开发环境)
DATABASE_URL=sqlite:///db.sqlite3

# PostgreSQL (生产环境)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# MySQL (生产环境)
DATABASE_URL=mysql://user:password@localhost:3306/dbname
```

#### Azure 存储配置
```bash
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=youraccount;AccountKey=yourkey;EndpointSuffix=core.windows.net
```

#### 加密配置
```bash
# 生成安全的加密密钥
ENCRYPTION_KEY=your-32-character-encryption-key
DECRYPTION_KEY=your-32-character-decryption-key
```

#### JWT 配置
```bash
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DELTA=3600
```

### 3. 生成安全密钥

#### Django SECRET_KEY
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

#### 加密密钥
```python
import secrets
print(secrets.token_hex(32))
```

### 4. 生产环境安全配置

#### 设置文件安全配置
```python
# settings.py
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 如果使用 PostgreSQL
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(os.getenv('DATABASE_URL'))
```

### 5. 安全最佳实践

#### 1. 永远不要提交敏感信息
- ✅ 使用环境变量
- ❌ 硬编码密钥和密码
- ❌ 提交 `.env` 文件

#### 2. 使用强密码
- 至少 32 个字符
- 包含大小写字母、数字、特殊字符
- 定期更换

#### 3. 生产环境配置
- 设置 `DEBUG=False`
- 配置 `ALLOWED_HOSTS`
- 使用 HTTPS
- 配置安全头

#### 4. 数据库安全
- 使用强密码
- 限制数据库访问
- 定期备份
- 加密敏感数据

### 6. 部署检查清单

- [ ] 所有敏感信息使用环境变量
- [ ] 设置 `DEBUG=False`
- [ ] 配置 `ALLOWED_HOSTS`
- [ ] 使用 HTTPS
- [ ] 配置安全头
- [ ] 定期更新依赖
- [ ] 监控安全日志
- [ ] 备份数据库

### 7. 常见安全问题

#### 1. 硬编码密钥
```python
# ❌ 错误做法
SECRET_KEY = "hardcoded-secret-key"

# ✅ 正确做法
SECRET_KEY = os.getenv('SECRET_KEY')
```

#### 2. 调试信息泄露
```python
# ❌ 生产环境
DEBUG = True

# ✅ 生产环境
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
```

#### 3. 数据库密码
```python
# ❌ 错误做法
DATABASES = {
    'default': {
        'PASSWORD': 'hardcoded-password'
    }
}

# ✅ 正确做法
DATABASES = {
    'default': {
        'PASSWORD': os.getenv('DB_PASSWORD')
    }
}
```

## 紧急情况处理

如果发现敏感信息已提交到 Git：

1. **立即更换密钥**
2. **从 Git 历史中移除敏感信息**
3. **通知相关团队**
4. **检查访问日志**

```bash
# 从 Git 历史中移除敏感文件
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch .env' \
--prune-empty --tag-name-filter cat -- --all
```
