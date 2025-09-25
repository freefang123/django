from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType

class MenuItem(models.Model):
    """菜单项模型"""
    MENU_TYPE_CHOICES = [
        ('menu', '菜单'),
        ('submenu', '子菜单'),
        ('action', '操作'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="菜单名称")
    title = models.CharField(max_length=100, verbose_name="菜单标题")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="图标")
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name="链接地址")
    component = models.CharField(max_length=200, blank=True, null=True, verbose_name="组件路径")
    menu_type = models.CharField(max_length=20, choices=MENU_TYPE_CHOICES, default='menu', verbose_name="菜单类型")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="父菜单")
    order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    description = models.TextField(blank=True, null=True, verbose_name="描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'permission_menuitem'
        verbose_name = "菜单项"
        verbose_name_plural = "菜单项"
        ordering = ['order', 'name']

class MenuPermission(models.Model):
    """菜单权限模型"""
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="菜单")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, verbose_name="用户组")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, verbose_name="用户")
    permission = models.CharField(max_length=100, blank=True, null=True, verbose_name="权限代码")
    is_active = models.BooleanField(default=True, verbose_name="是否激活")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        if self.group:
            return f"{self.menu.title} - {self.group.name}"
        elif self.user:
            return f"{self.menu.title} - {self.user.username}"
        else:
            return f"{self.menu.title} - {self.permission}"
    
    class Meta:
        db_table = 'permission_menupermission'
        verbose_name = "菜单权限"
        verbose_name_plural = "菜单权限"
        unique_together = ['menu', 'group', 'user']

class UserMenuLog(models.Model):
    """用户菜单访问日志"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    menu = models.ForeignKey(MenuItem, on_delete=models.CASCADE, verbose_name="菜单")
    action = models.CharField(max_length=50, verbose_name="操作")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    user_agent = models.TextField(blank=True, null=True, verbose_name="用户代理")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return f"{self.user.username} - {self.menu.title} - {self.action}"
    
    class Meta:
        db_table = 'permission_usermenulog'
        verbose_name = "用户菜单日志"
        verbose_name_plural = "用户菜单日志"
        ordering = ['-created_at']
