# Django权限管理系统使用指南

## 概述

本项目实现了基于Django内置权限系统的完整权限管理解决方案，包括用户、组、权限的管理，以及权限控制装饰器。

## 功能特性

### 1. 用户管理
- 用户创建、编辑、删除
- 用户档案管理
- 用户权限分配
- 用户组分配

### 2. 组管理
- 组创建、编辑、删除
- 组权限分配
- 用户组管理

### 3. 权限管理
- 权限查看和分配
- 权限日志记录
- 权限统计

### 4. 权限控制
- 装饰器权限控制
- API权限验证
- 权限日志记录

## API接口

### 用户管理接口

#### 获取用户列表
```
GET /api/permission/users/
Authorization: Bearer <token>
```

#### 创建用户
```
POST /api/permission/users/create/
Authorization: Bearer <token>
Content-Type: application/json

{
    "username": "newuser",
    "email": "user@example.com",
    "password": "password123",
    "confirm_password": "password123",
    "first_name": "John",
    "last_name": "Doe",
    "profile": {
        "phone": "1234567890",
        "department": "IT",
        "position": "Developer"
    }
}
```

#### 获取用户详情
```
GET /api/permission/users/{id}/
Authorization: Bearer <token>
```

### 组管理接口

#### 获取组列表
```
GET /api/permission/groups/
Authorization: Bearer <token>
```

#### 创建组
```
POST /api/permission/groups/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "developers",
    "permissions": [1, 2, 3]
}
```

### 权限管理接口

#### 获取权限列表
```
GET /api/permission/permissions/
Authorization: Bearer <token>
```

#### 分配组权限
```
POST /api/permission/assign-group-permissions/
Authorization: Bearer <token>
Content-Type: application/json

{
    "group_id": 1,
    "permission_ids": [1, 2, 3]
}
```

#### 分配用户组
```
POST /api/permission/assign-user-groups/
Authorization: Bearer <token>
Content-Type: application/json

{
    "user_id": 1,
    "group_ids": [1, 2]
}
```

#### 分配用户权限
```
POST /api/permission/assign-user-permissions/
Authorization: Bearer <token>
Content-Type: application/json

{
    "user_id": 1,
    "permission_ids": [1, 2, 3]
}
```

### 权限查询接口

#### 获取当前用户权限
```
GET /api/permission/user-permissions/
Authorization: Bearer <token>
```

#### 获取权限统计
```
GET /api/permission/permission-stats/
Authorization: Bearer <token>
```

### 日志管理接口

#### 获取权限日志
```
GET /api/permission/logs/
Authorization: Bearer <token>

# 查询参数
?user_id=1&action=login&page=1
```

## 权限装饰器使用

### 1. 权限装饰器

```python
from utils.permission_utils import require_permission

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_permission('api.view_account')
def get_accounts(request):
    # 需要 api.view_account 权限
    pass
```

### 2. 组装饰器

```python
from utils.permission_utils import require_group

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_group('developers')
def create_project(request):
    # 需要 developers 组权限
    pass
```

### 3. 任意组装饰器

```python
from utils.permission_utils import require_any_group

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_any_group('developers', 'managers')
def view_reports(request):
    # 需要 developers 或 managers 组权限
    pass
```

### 4. 超级用户装饰器

```python
from utils.permission_utils import require_superuser

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@require_superuser
def delete_user(request):
    # 需要超级用户权限
    pass
```

### 5. 员工装饰器

```python
from utils.permission_utils import require_staff

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@require_staff
def admin_panel(request):
    # 需要员工权限
    pass
```

## 权限管理后台

访问 Django 管理后台：`http://localhost:8000/admin/`

### 功能包括：
1. **用户管理** - 查看、编辑用户信息
2. **组管理** - 管理用户组和权限
3. **权限管理** - 查看所有权限
4. **权限日志** - 查看权限操作日志

## 权限配置示例

### 1. 创建权限组

```python
from django.contrib.auth.models import Group, Permission

# 创建开发者组
developers_group = Group.objects.create(name='developers')

# 添加权限
permissions = Permission.objects.filter(codename__in=[
    'add_account',
    'change_account', 
    'view_account'
])
developers_group.permissions.set(permissions)
```

### 2. 分配用户到组

```python
from django.contrib.auth.models import User

user = User.objects.get(username='developer')
user.groups.add(developers_group)
```

### 3. 直接分配权限

```python
from django.contrib.auth.models import Permission

permission = Permission.objects.get(codename='add_account')
user.user_permissions.add(permission)
```

## 权限检查

### 1. 检查权限

```python
from django.contrib.auth.models import User

user = User.objects.get(username='developer')

# 检查特定权限
if user.has_perm('api.add_account'):
    print("用户有添加账户权限")

# 检查组权限
if user.groups.filter(name='developers').exists():
    print("用户属于开发者组")
```

### 2. 在视图中检查权限

```python
from django.contrib.auth.decorators import permission_required

@permission_required('api.add_account')
def create_account(request):
    # 只有拥有 api.add_account 权限的用户才能访问
    pass
```

## 权限日志

系统会自动记录以下权限操作：
- 用户登录/登出
- 权限授予/撤销
- 组添加/移除
- 访问被拒绝/允许

日志包含：
- 操作用户
- 操作类型
- 资源信息
- IP地址
- 用户代理
- 操作结果
- 时间戳

## 最佳实践

### 1. 权限命名规范
- 使用应用名.操作_模型名 格式
- 例如：`api.add_account`, `api.view_account`, `api.change_account`

### 2. 组权限管理
- 按角色创建组（如：developers, managers, admins）
- 为组分配相关权限
- 将用户分配到相应组

### 3. 权限检查
- 在视图函数开始处检查权限
- 使用装饰器简化权限检查
- 记录权限操作日志

### 4. 安全建议
- 定期审查权限分配
- 监控权限操作日志
- 及时撤销不必要的权限
- 使用最小权限原则

## 故障排除

### 1. 权限不生效
- 检查用户是否已登录
- 确认权限名称正确
- 验证用户是否属于相应组
- 检查权限是否已激活

### 2. 装饰器不工作
- 确保装饰器顺序正确
- 检查权限名称格式
- 验证用户认证状态

### 3. 日志记录问题
- 检查数据库连接
- 验证日志模型配置
- 查看错误日志

## 扩展功能

### 1. 自定义权限类
```python
from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

### 2. 权限中间件
```python
class PermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # 权限检查逻辑
        response = self.get_response(request)
        return response
```

### 3. 权限缓存
```python
from django.core.cache import cache

def get_user_permissions(user):
    cache_key = f'user_permissions_{user.id}'
    permissions = cache.get(cache_key)
    if not permissions:
        permissions = user.get_all_permissions()
        cache.set(cache_key, permissions, 300)  # 缓存5分钟
    return permissions
```

这个权限管理系统提供了完整的用户权限管理功能，包括权限分配、权限检查、日志记录等。通过装饰器和API接口，可以灵活地控制业务接口的访问权限。
