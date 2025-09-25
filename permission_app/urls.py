from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # 权限管理页面
    path('admin/', views.permission_admin_view, name='permission-admin'),
    
    # 用户管理
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateView.as_view(), name='user-create'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    
    # 组管理
    path('groups/', views.GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', views.GroupDetailView.as_view(), name='group-detail'),
    
    # 权限管理
    path('permissions/', views.PermissionListView.as_view(), name='permission-list'),
    
    # 权限分配
    path('assign-group-permissions/', views.assign_group_permissions, name='assign-group-permissions'),
    path('assign-user-groups/', views.assign_user_groups, name='assign-user-groups'),
    path('assign-user-permissions/', views.assign_user_permissions, name='assign-user-permissions'),
    
    # 权限查询
    path('user-permissions/', views.user_permissions, name='user-permissions'),
    path('permission-stats/', views.permission_stats, name='permission-stats'),
    
    # 日志管理
    path('logs/', views.PermissionLogListView.as_view(), name='permission-log-list'),
    
    # 菜单管理
    path('menus/', views.MenuItemListView.as_view(), name='menu-list'),
    path('menus/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-detail'),
    path('menus/tree/', views.MenuTreeView.as_view(), name='menu-tree'),
    path('user-menu/', views.user_menu_view, name='user-menu'),
    path('assign-user-menus/', views.assign_user_menus, name='assign-user-menus'),
    path('assign-group-menus/', views.assign_group_menus, name='assign-group-menus'),
    path('menu-permissions/', views.menu_permissions, name='menu-permissions'),
    path('menu-logs/', views.menu_logs, name='menu-logs'),
    path('log-menu-access/', views.log_menu_access, name='log-menu-access'),
    
    # 菜单树管理
    path('menu-tree/', admin_views.menu_tree_view, name='menu-tree'),
    path('menu-tree-api/', admin_views.menu_tree_api, name='menu-tree-api'),
    path('menu-permissions/', admin_views.menu_permissions_view, name='menu-permissions'),
    path('menu-logs-view/', admin_views.menu_logs_view, name='menu-logs-view'),
]
