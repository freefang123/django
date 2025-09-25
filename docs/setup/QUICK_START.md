# Django权限管理系统快速启动指南

## 快速开始

### 1. 启动Django服务器
```bash
cd D:\program\Django\myproject
python manage.py runserver
```

### 2. 访问权限管理页面
打开浏览器访问：`http://localhost:8000/api/permission/admin/`

### 3. 使用测试账户登录
- **用户名**: `testuser1`, **密码**: `password123` (开发者组)
- **用户名**: `testuser2`, **密码**: `password123` (管理员组)
- **用户名**: `admin`, **密码**: `admin123` (超级用户)

## 主要功能

### 1. 权限管理页面
- 仪表板：显示系统统计信息
- 用户管理：查看、编辑用户信息
- 组管理：管理用户组和权限
- 权限管理：查看所有权限
- 权限日志：查看权限操作记录

### 2. API接口
- 用户管理：`/api/permission/users/`
- 组管理：`/api/permission/groups/`
- 权限管理：`/api/permission/permissions/`
- 权限分配：`/api/permission/assign-*`
- 权限查询：`/api/permission/user-permissions/`

### 3. 权限控制装饰器
```python
from utils.permission_utils import require_permission, require_group

@require_permission('api.view_account')
def get_accounts(request):
    pass

@require_group('developers')
def create_project(request):
    pass
```

## 测试功能

### 1. 运行权限系统测试
```bash
python test_permissions.py
```

### 2. 运行API测试
```bash
python test_permission_api.py
```

### 3. 访问Django管理后台
`http://localhost:8000/admin/`

## 权限配置示例

### 1. 创建组和权限
```python
from django.contrib.auth.models import Group, Permission

# 创建开发者组
developers = Group.objects.create(name='developers')

# 分配权限
permissions = Permission.objects.filter(codename__in=[
    'add_account', 'change_account', 'view_account'
])
developers.permissions.set(permissions)
```

### 2. 分配用户到组
```python
from django.contrib.auth.models import User

user = User.objects.get(username='testuser1')
user.groups.add(developers)
```

### 3. 检查权限
```python
user = User.objects.get(username='testuser1')

# 检查权限
if user.has_perm('api.add_account'):
    print("用户有添加账户权限")

# 检查组
if user.groups.filter(name='developers').exists():
    print("用户属于开发者组")
```

## 常用API接口

### 1. 获取用户权限
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/permission/user-permissions/
```

### 2. 获取权限统计
```bash
curl -H "Authorization: Bearer <token>" \
     http://localhost:8000/api/permission/permission-stats/
```

### 3. 分配组权限
```bash
curl -X POST \
     -H "Authorization: Bearer <token>" \
     -H "Content-Type: application/json" \
     -d '{"group_id": 1, "permission_ids": [1,2,3]}' \
     http://localhost:8000/api/permission/assign-group-permissions/
```

## 故障排除

### 1. 权限不生效
- 检查用户是否已登录
- 确认权限名称正确
- 验证用户是否属于相应组

### 2. 装饰器不工作
- 确保装饰器顺序正确
- 检查权限名称格式
- 验证用户认证状态

### 3. 页面无法访问
- 检查Django服务器是否运行
- 确认URL路径正确
- 查看浏览器控制台错误

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

## 安全建议

1. **定期审查权限分配**
2. **监控权限操作日志**
3. **及时撤销不必要的权限**
4. **使用最小权限原则**
5. **定期更新密码**

## 技术支持

如有问题，请查看：
- `PERMISSION_GUIDE.md` - 详细使用指南
- `PERMISSION_SUMMARY.md` - 实现总结
- Django官方文档：https://docs.djangoproject.com/
- Django REST Framework文档：https://www.django-rest-framework.org/

## 更新日志

- **v1.0.0** - 初始版本，包含基本权限管理功能
- 用户管理、组管理、权限分配
- 权限控制装饰器
- 权限日志记录
- Web管理界面
- API接口
