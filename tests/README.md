# 测试文件说明

本文件夹包含项目的所有测试用例文件。

## 测试文件列表

- `test_admin_menu_tree.py` - Django管理后台菜单树功能测试
- `test_api.py` - API接口测试
- `test_jwt_auth.py` - JWT认证测试
- `test_menu_api.py` - 菜单API测试
- `test_menu_tree.py` - 菜单树功能测试
- `test_menu_tree_page.py` - 菜单树页面测试
- `test_permission_api.py` - 权限API测试
- `test_permissions.py` - 权限功能测试

## 运行测试

### 运行所有测试
```bash
python -m pytest tests/
```

### 运行特定测试
```bash
# 运行菜单树测试
python tests/test_menu_tree.py

# 运行API测试
python tests/test_api.py

# 运行权限测试
python tests/test_permissions.py
```

### 运行Django管理后台测试
```bash
# 确保Django服务器正在运行
python manage.py runserver

# 在另一个终端运行测试
python tests/test_admin_menu_tree.py
```

## 测试说明

- 所有测试文件都是独立的，可以单独运行
- 测试前请确保Django服务器正在运行
- 某些测试需要数据库中有相应的测试数据
- 测试结果会显示在控制台中，包括成功和失败的详细信息
