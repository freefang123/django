# Django动态菜单系统使用指南

## 概述

本项目实现了基于权限的动态菜单系统，不同权限的用户看到不同的菜单。根据您的需求：

- **经理组 (managers)**: 包含人员设置和在线聊天两个菜单
- **开发者组 (developers)**: 只有在线聊天菜单
- **超级用户 (admin)**: 拥有所有菜单权限

## 功能特性

### 1. 菜单管理
- 菜单项创建、编辑、删除
- 菜单树结构管理
- 菜单权限分配
- 菜单访问日志

### 2. 权限控制
- 基于用户组的菜单权限
- 基于用户的菜单权限
- 基于权限代码的菜单权限
- 动态菜单生成

### 3. 菜单结构
- 支持多级菜单
- 菜单图标和链接
- 组件路径配置
- 菜单排序

## API接口

### 1. 获取用户菜单
```
GET /api/permission/user-menu/
Authorization: Bearer <token>
```

**响应示例：**
```json
{
    "success": true,
    "menus": [
        {
            "id": 1,
            "name": "main",
            "title": "主菜单",
            "icon": "menu",
            "url": null,
            "component": null,
            "menu_type": "menu",
            "order": 0,
            "children": [
                {
                    "id": 2,
                    "name": "personnel",
                    "title": "人员设置",
                    "icon": "users",
                    "url": "/personnel",
                    "component": "PersonnelManagement",
                    "menu_type": "menu",
                    "order": 1,
                    "children": [
                        {
                            "id": 4,
                            "name": "personnel_list",
                            "title": "人员列表",
                            "icon": "list",
                            "url": "/personnel/list",
                            "component": "PersonnelList",
                            "menu_type": "submenu",
                            "order": 1,
                            "children": []
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "chat",
                    "title": "在线聊天",
                    "icon": "message-circle",
                    "url": "/chat",
                    "component": "ChatRoom",
                    "menu_type": "menu",
                    "order": 2,
                    "children": [
                        {
                            "id": 6,
                            "name": "chat_room",
                            "title": "聊天室",
                            "icon": "message-square",
                            "url": "/chat/room",
                            "component": "ChatRoom",
                            "menu_type": "submenu",
                            "order": 1,
                            "children": []
                        }
                    ]
                }
            ]
        }
    ],
    "user": {
        "id": 1,
        "username": "testuser1",
        "is_superuser": false,
        "is_staff": false
    }
}
```

### 2. 菜单管理接口

#### 获取菜单列表
```
GET /api/permission/menus/
Authorization: Bearer <token>
```

#### 获取菜单树
```
GET /api/permission/menus/tree/
Authorization: Bearer <token>
```

#### 创建菜单
```
POST /api/permission/menus/
Authorization: Bearer <token>
Content-Type: application/json

{
    "name": "new_menu",
    "title": "新菜单",
    "icon": "plus",
    "url": "/new-menu",
    "component": "NewMenu",
    "menu_type": "menu",
    "parent": null,
    "order": 0,
    "is_active": true,
    "description": "新菜单描述"
}
```

#### 更新菜单
```
PUT /api/permission/menus/{id}/
Authorization: Bearer <token>
Content-Type: application/json

{
    "title": "更新后的菜单标题",
    "order": 1
}
```

#### 删除菜单
```
DELETE /api/permission/menus/{id}/
Authorization: Bearer <token>
```

### 3. 菜单权限管理

#### 分配用户菜单
```
POST /api/permission/assign-user-menus/
Authorization: Bearer <token>
Content-Type: application/json

{
    "user_id": 1,
    "menu_ids": [1, 2, 3]
}
```

#### 分配组菜单
```
POST /api/permission/assign-group-menus/
Authorization: Bearer <token>
Content-Type: application/json

{
    "group_id": 1,
    "menu_ids": [1, 2, 3]
}
```

#### 获取菜单权限列表
```
GET /api/permission/menu-permissions/
Authorization: Bearer <token>
```

### 4. 菜单日志

#### 获取菜单访问日志
```
GET /api/permission/menu-logs/
Authorization: Bearer <token>
```

#### 记录菜单访问
```
POST /api/permission/log-menu-access/
Authorization: Bearer <token>
Content-Type: application/json

{
    "menu_id": 1,
    "action": "access"
}
```

## 菜单配置

### 1. 菜单结构
```
主菜单
├── 人员设置
│   ├── 人员列表
│   └── 添加人员
└── 在线聊天
    ├── 聊天室
    └── 聊天记录
```

### 2. 权限分配
- **经理组 (managers)**: 人员设置 + 在线聊天
- **开发者组 (developers)**: 仅在线聊天
- **超级用户 (admin)**: 所有菜单

### 3. 菜单字段说明
- `name`: 菜单名称（唯一标识）
- `title`: 菜单显示标题
- `icon`: 菜单图标
- `url`: 菜单链接地址
- `component`: 前端组件路径
- `menu_type`: 菜单类型（menu/submenu/action）
- `parent`: 父菜单ID
- `order`: 排序顺序
- `is_active`: 是否激活

## 使用示例

### 1. 前端集成

```javascript
// 获取用户菜单
async function getUserMenus() {
    const response = await fetch('/api/permission/user-menu/', {
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    const data = await response.json();
    return data.menus;
}

// 渲染菜单
function renderMenu(menus) {
    const menuContainer = document.getElementById('menu-container');
    
    menus.forEach(menu => {
        const menuItem = document.createElement('div');
        menuItem.className = 'menu-item';
        menuItem.innerHTML = `
            <i class="icon ${menu.icon}"></i>
            <span>${menu.title}</span>
        `;
        
        if (menu.url) {
            menuItem.addEventListener('click', () => {
                window.location.href = menu.url;
            });
        }
        
        menuContainer.appendChild(menuItem);
        
        // 渲染子菜单
        if (menu.children && menu.children.length > 0) {
            const submenu = document.createElement('div');
            submenu.className = 'submenu';
            menu.children.forEach(child => {
                const submenuItem = document.createElement('div');
                submenuItem.className = 'submenu-item';
                submenuItem.innerHTML = `
                    <i class="icon ${child.icon}"></i>
                    <span>${child.title}</span>
                `;
                submenu.appendChild(submenuItem);
            });
            menuContainer.appendChild(submenu);
        }
    });
}
```

### 2. 菜单权限检查

```python
from permission_app.views import get_user_menus

def check_menu_permission(user, menu_name):
    """检查用户是否有菜单权限"""
    user_menus = get_user_menus(user)
    
    for menu in user_menus:
        if menu['name'] == menu_name:
            return True
        # 检查子菜单
        for child in menu.get('children', []):
            if child['name'] == menu_name:
                return True
    
    return False
```

### 3. 菜单访问日志

```python
from permission_app.models import UserMenuLog

def log_menu_access(user, menu, action='access'):
    """记录菜单访问日志"""
    UserMenuLog.objects.create(
        user=user,
        menu=menu,
        action=action,
        ip_address=request.META.get('REMOTE_ADDR'),
        user_agent=request.META.get('HTTP_USER_AGENT', '')
    )
```

## 测试功能

### 1. 运行菜单初始化
```bash
python init_menu_data.py
```

### 2. 运行菜单API测试
```bash
python test_menu_api.py
```

### 3. 访问Django管理后台
```
http://localhost:8000/admin/
```

## 扩展功能

### 1. 自定义菜单权限
```python
from permission_app.models import MenuPermission

# 基于权限代码的菜单权限
MenuPermission.objects.create(
    menu=menu,
    permission='api.view_personnel',
    is_active=True
)
```

### 2. 菜单缓存
```python
from django.core.cache import cache

def get_cached_user_menus(user):
    cache_key = f'user_menus_{user.id}'
    menus = cache.get(cache_key)
    if not menus:
        menus = get_user_menus(user)
        cache.set(cache_key, menus, 300)  # 缓存5分钟
    return menus
```

### 3. 菜单权限中间件
```python
class MenuPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith('/api/permission/user-menu'):
            # 检查菜单权限
            pass
        
        response = self.get_response(request)
        return response
```

## 最佳实践

### 1. 菜单设计
- 使用清晰的菜单名称和标题
- 合理设置菜单层级
- 使用合适的图标
- 保持菜单结构简洁

### 2. 权限管理
- 基于角色分配菜单权限
- 定期审查菜单权限
- 记录菜单访问日志
- 使用最小权限原则

### 3. 性能优化
- 使用菜单缓存
- 优化数据库查询
- 减少不必要的菜单检查
- 使用CDN加载图标

### 4. 安全考虑
- 验证菜单权限
- 防止权限提升
- 记录敏感操作
- 定期安全审计

## 故障排除

### 1. 菜单不显示
- 检查用户权限
- 验证菜单是否激活
- 确认菜单权限分配
- 查看错误日志

### 2. 权限不生效
- 检查用户组分配
- 验证菜单权限配置
- 确认权限缓存
- 重新分配权限

### 3. 菜单访问慢
- 检查数据库查询
- 优化菜单树构建
- 使用菜单缓存
- 减少菜单层级

## 总结

这个动态菜单系统提供了完整的菜单管理功能，包括：

1. **灵活的菜单结构** - 支持多级菜单和子菜单
2. **细粒度权限控制** - 基于用户、组、权限的菜单控制
3. **完整的API接口** - 菜单管理、权限分配、日志记录
4. **详细的访问日志** - 记录所有菜单访问操作
5. **易于扩展** - 支持自定义菜单权限和中间件

通过这个系统，您可以轻松地实现基于权限的动态菜单，为不同角色的用户提供不同的菜单体验。
