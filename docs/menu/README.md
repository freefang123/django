# 菜单系统文档

本文件夹包含菜单系统相关的所有文档。

## 文档列表

- `MENU_GUIDE.md` - 菜单系统使用指南
- `MENU_SUMMARY.md` - 菜单系统功能总结
- `MENU_TREE_FINAL.md` - 菜单树最终实现说明
- `MENU_TREE_GUIDE.md` - 菜单树使用指南
- `ADMIN_MENU_TREE_FIXED.md` - 管理后台菜单树修复说明

## 功能说明

菜单系统提供以下功能：
- 树状菜单结构管理
- 菜单权限控制
- 用户菜单访问日志
- 管理后台菜单树显示

## 使用指南

1. **基础使用**：查看 `MENU_GUIDE.md`
2. **树状结构**：查看 `MENU_TREE_GUIDE.md`
3. **功能总结**：查看 `MENU_SUMMARY.md`
4. **问题修复**：查看 `ADMIN_MENU_TREE_FIXED.md`

## 开发说明

- 菜单数据存储在 `permission_app` 应用中
- 支持多级菜单结构
- 提供RESTful API接口
- 集成Django管理后台
