# 数据库表前缀配置说明

## 📋 **当前配置**

### 数据库连接配置
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## 🔧 **表前缀配置方法**

### 方法1：使用 `db_table` 在模型中指定（推荐）

```python
# models/user_models.py
class Account(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()
    
    class Meta:
        db_table = 'myproject_account'  # 指定表名
        verbose_name = "账户"
        verbose_name_plural = "账户"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'myproject_userprofile'  # 指定表名
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案"
```

### 方法2：使用自定义数据库路由

创建 `database_routers.py` 文件：

```python
# database_routers.py
class DatabaseRouter:
    def db_for_read(self, model, **hints):
        return 'default'
    
    def db_for_write(self, model, **hints):
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return True
```

然后在 `settings.py` 中添加：

```python
DATABASE_ROUTERS = ['path.to.database_routers.DatabaseRouter']
```

### 方法3：使用环境变量配置

```python
# settings.py
import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'test'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'root'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
```

## 📊 **当前表结构**

### Django默认表
- `auth_user` - 用户表
- `auth_group` - 用户组表
- `auth_permission` - 权限表
- `django_admin_log` - 管理日志表
- `django_content_type` - 内容类型表
- `django_session` - 会话表
- `django_migrations` - 迁移记录表

### 自定义表（带前缀）
- `myproject_account` - 账户表
- `myproject_userprofile` - 用户档案表

## ✅ **迁移状态**

### 当前迁移状态
```bash
$ python manage.py showmigrations
admin
 [X] 0001_initial
 [X] 0002_logentry_remove_auto_add
 [X] 0003_logentry_add_action_flag_choices
auth
 [X] 0001_initial
 [X] 0002_alter_permission_name_max_length
 [X] 0003_alter_user_email_max_length
 [X] 0004_alter_user_username_opts
 [X] 0005_alter_user_last_login_null
 [X] 0006_require_contenttypes_0002
 [X] 0007_alter_validators_add_error_messages
 [X] 0008_alter_user_username_max_length
 [X] 0009_alter_user_last_name_max_length
 [X] 0010_alter_group_name_max_length
 [X] 0011_update_proxy_permissions
 [X] 0012_alter_user_first_name_max_length
contenttypes
 [X] 0001_initial
 [X] 0002_remove_content_type_name
models
 [X] 0001_initial
sessions
 [X] 0001_initial
```

### 数据库表验证
```bash
# 检查表是否存在
SHOW TABLES LIKE 'myproject_%';

# 结果：
# myproject_account
# myproject_userprofile
```

## 🛠️ **重新生成迁移文件的步骤**

### 1. 删除现有迁移文件
```bash
rm models/migrations/0001_initial.py
```

### 2. 重置迁移状态
```bash
python manage.py migrate --fake models zero
```

### 3. 重新生成迁移
```bash
python manage.py makemigrations models
```

### 4. 应用迁移
```bash
python manage.py migrate
```

### 5. 如果表已存在，使用fake标记
```bash
python manage.py migrate --fake models
```

## 🎯 **表前缀的最佳实践**

### 1. **命名规范**
- 使用项目名称作为前缀：`myproject_`
- 使用模块名称作为前缀：`api_`, `auth_`
- 使用功能名称作为前缀：`user_`, `order_`

### 2. **配置示例**

```python
# 不同模块使用不同前缀
class Account(models.Model):
    class Meta:
        db_table = 'api_account'

class UserProfile(models.Model):
    class Meta:
        db_table = 'auth_userprofile'

class Order(models.Model):
    class Meta:
        db_table = 'order_main'
```

### 3. **环境变量配置**

```python
# settings.py
import os

DB_PREFIX = os.getenv('DB_PREFIX', 'myproject')

# 在模型中动态使用
class Account(models.Model):
    class Meta:
        db_table = f'{DB_PREFIX}_account'
```

## ✅ **验证配置**

### 1. 检查迁移文件
```bash
python manage.py showmigrations
```

### 2. 检查数据库表
```sql
-- MySQL
SHOW TABLES LIKE 'myproject_%';

-- 或者查看所有表
SHOW TABLES;
```

### 3. 检查表结构
```sql
DESCRIBE myproject_account;
DESCRIBE myproject_userprofile;
```

### 4. 测试模型
```python
# 在Django shell中测试
python manage.py shell

>>> from models.user_models import Account, UserProfile
>>> account = Account.objects.create(name="测试", age=25, email="test@example.com")
>>> print(account)
```

## 🚀 **总结**

表前缀配置主要通过以下方式实现：

1. **模型级别**：在模型的 `Meta` 类中设置 `db_table`
2. **迁移文件**：确保迁移文件包含正确的 `db_table` 选项
3. **数据库级别**：通过数据库路由或环境变量进行全局配置

### ✅ **当前项目配置状态**

- ✅ 迁移文件已正确生成
- ✅ 数据库表已成功创建
- ✅ 表前缀配置正确：`myproject_`
- ✅ 模型测试通过

**当前项目已配置的表前缀：**
- `myproject_account` - 账户表
- `myproject_userprofile` - 用户档案表