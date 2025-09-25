from django.contrib import admin
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import UserProfile, PermissionLog, MenuItem, MenuPermission, UserMenuLog

class UserProfileInline(admin.StackedInline):
    """用户档案内联"""
    model = UserProfile
    can_delete = False
    verbose_name_plural = '用户档案'

class CustomUserAdmin(UserAdmin):
    """自定义用户管理"""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)

class PermissionLogAdmin(admin.ModelAdmin):
    """权限日志管理"""
    list_display = ('user', 'action', 'resource', 'permission', 'ip_address', 'success', 'created_at')
    list_filter = ('action', 'success', 'created_at', 'user')
    search_fields = ('user__username', 'resource', 'permission', 'ip_address')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

class CustomGroupAdmin(GroupAdmin):
    """自定义组管理"""
    list_display = ('name', 'permission_count', 'user_count')
    
    def permission_count(self, obj):
        return obj.permissions.count()
    permission_count.short_description = '权限数量'
    
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = '用户数量'

# 重新注册管理类
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Group, CustomGroupAdmin)
admin.site.register(PermissionLog, PermissionLogAdmin)

# 权限管理
admin.site.register(Permission)

# 菜单管理
class MenuItemAdmin(admin.ModelAdmin):
    """菜单项管理"""
    list_display = ('title', 'name', 'menu_type', 'parent', 'order', 'is_active', 'get_children_count')
    list_filter = ('menu_type', 'is_active', 'parent')
    search_fields = ('name', 'title', 'url')
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    list_per_page = 50
    
    def get_children_count(self, obj):
        """获取子菜单数量"""
        return obj.menuitem_set.count()
    get_children_count.short_description = '子菜单数量'
    
    def get_queryset(self, request):
        """优化查询"""
        return super().get_queryset(request).select_related('parent').prefetch_related('menuitem_set')
    
    def changelist_view(self, request, extra_context=None):
        """自定义列表视图，显示树状结构"""
        extra_context = extra_context or {}
        extra_context['menu_tree'] = self.get_menu_tree_data()
        
        # 添加统计信息
        extra_context['active_count'] = MenuItem.objects.filter(is_active=True).count()
        extra_context['root_count'] = MenuItem.objects.filter(parent__isnull=True).count()
        
        return super().changelist_view(request, extra_context)
    
    def get_menu_tree_data(self):
        """获取菜单树数据"""
        from django.db.models import Prefetch
        
        # 获取根菜单及其子菜单
        root_menus = MenuItem.objects.filter(
            parent__isnull=True
        ).prefetch_related(
            Prefetch('menuitem_set', queryset=MenuItem.objects.filter(is_active=True).order_by('order'))
        ).order_by('order')
        
        return root_menus

class MenuPermissionAdmin(admin.ModelAdmin):
    """菜单权限管理"""
    list_display = ('menu', 'group', 'user', 'permission', 'is_active')
    list_filter = ('is_active', 'menu', 'group')
    search_fields = ('menu__title', 'group__name', 'user__username', 'permission')
    ordering = ('-created_at',)

class UserMenuLogAdmin(admin.ModelAdmin):
    """用户菜单日志管理"""
    list_display = ('user', 'menu', 'action', 'ip_address', 'created_at')
    list_filter = ('action', 'created_at', 'user', 'menu')
    search_fields = ('user__username', 'menu__title', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(MenuPermission, MenuPermissionAdmin)
admin.site.register(UserMenuLog, UserMenuLogAdmin)
