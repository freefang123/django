from rest_framework import serializers
from django.contrib.auth.models import User, Group
from .menu_models import MenuItem, MenuPermission, UserMenuLog

class MenuItemSerializer(serializers.ModelSerializer):
    """菜单项序列化器"""
    children = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'title', 'icon', 'url', 'component', 'menu_type', 
                 'parent', 'order', 'is_active', 'description', 'has_children', 'children']
    
    def get_children(self, obj):
        """获取子菜单"""
        children = obj.children.filter(is_active=True).order_by('order')
        return MenuItemSerializer(children, many=True, context=self.context).data
    
    def get_has_children(self, obj):
        """是否有子菜单"""
        return obj.children.filter(is_active=True).exists()

class MenuPermissionSerializer(serializers.ModelSerializer):
    """菜单权限序列化器"""
    menu_title = serializers.CharField(source='menu.title', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = MenuPermission
        fields = ['id', 'menu', 'menu_title', 'group', 'group_name', 'user', 'user_username', 
                 'permission', 'is_active', 'created_at']

class UserMenuLogSerializer(serializers.ModelSerializer):
    """用户菜单日志序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    menu_title = serializers.CharField(source='menu.title', read_only=True)
    
    class Meta:
        model = UserMenuLog
        fields = ['id', 'user', 'user_username', 'menu', 'menu_title', 'action', 
                 'ip_address', 'created_at']

class MenuTreeSerializer(serializers.ModelSerializer):
    """菜单树序列化器"""
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'title', 'icon', 'url', 'component', 'menu_type', 
                 'order', 'is_active', 'children']
    
    def get_children(self, obj):
        """获取子菜单"""
        children = obj.children.filter(is_active=True).order_by('order')
        return MenuTreeSerializer(children, many=True, context=self.context).data

class UserMenuSerializer(serializers.Serializer):
    """用户菜单序列化器"""
    user_id = serializers.IntegerField()
    menu_ids = serializers.ListField(child=serializers.IntegerField())

class GroupMenuSerializer(serializers.Serializer):
    """组菜单序列化器"""
    group_id = serializers.IntegerField()
    menu_ids = serializers.ListField(child=serializers.IntegerField())
