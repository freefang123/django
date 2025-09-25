from django.db import models
from django.contrib.auth.models import User, Group, Permission
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
    
    @property
    def children(self):
        """获取子菜单"""
        return MenuItem.objects.filter(parent=self, is_active=True).order_by('order')

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

class UserProfile(models.Model):
    """扩展用户档案模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='permission_profile')
    phone = models.CharField(max_length=15, blank=True, null=True, verbose_name="电话")
    avatar = models.URLField(blank=True, null=True, verbose_name="头像")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="部门")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="职位")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    class Meta:
        db_table = 'permission_userprofile'
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案"

class PermissionLog(models.Model):
    """权限操作日志"""
    ACTION_CHOICES = [
        ('login', '登录'),
        ('logout', '登出'),
        ('permission_granted', '授予权限'),
        ('permission_revoked', '撤销权限'),
        ('group_added', '加入组'),
        ('group_removed', '移除组'),
        ('access_denied', '访问被拒绝'),
        ('access_granted', '访问允许'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    action = models.CharField(max_length=20, choices=ACTION_CHOICES, verbose_name="操作类型")
    resource = models.CharField(max_length=200, verbose_name="资源")
    permission = models.CharField(max_length=100, blank=True, null=True, verbose_name="权限")
    group = models.CharField(max_length=100, blank=True, null=True, verbose_name="组")
    ip_address = models.GenericIPAddressField(verbose_name="IP地址")
    user_agent = models.TextField(blank=True, null=True, verbose_name="用户代理")
    success = models.BooleanField(default=True, verbose_name="是否成功")
    message = models.TextField(blank=True, null=True, verbose_name="消息")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    
    def __str__(self):
        return f"{self.user.username} - {self.get_action_display()} - {self.resource}"
    
    class Meta:
        db_table = 'permission_permissionlog'
        verbose_name = "权限日志"
        verbose_name_plural = "权限日志"
        ordering = ['-created_at']
