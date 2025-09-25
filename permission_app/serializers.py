from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import UserProfile, PermissionLog, MenuItem, MenuPermission, UserMenuLog

class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type', 'content_type_name']

class GroupSerializer(serializers.ModelSerializer):
    """组序列化器"""
    permissions = PermissionSerializer(many=True, read_only=True)
    permission_count = serializers.SerializerMethodField()
    user_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions', 'permission_count', 'user_count']
    
    def get_permission_count(self, obj):
        return obj.permissions.count()
    
    def get_user_count(self, obj):
        return obj.user_set.count()

class UserProfileSerializer(serializers.ModelSerializer):
    """用户档案序列化器"""
    class Meta:
        model = UserProfile
        fields = ['phone', 'avatar', 'department', 'position', 'created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    profile = UserProfileSerializer(read_only=True)
    groups = GroupSerializer(many=True, read_only=True)
    user_permissions = PermissionSerializer(many=True, read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 
                 'is_superuser', 'date_joined', 'last_login', 'profile', 'groups', 'user_permissions']
        read_only_fields = ['id', 'date_joined', 'last_login']

class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'confirm_password', 'profile']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError("密码不匹配")
        return attrs
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        validated_data.pop('confirm_password')
        
        user = User.objects.create_user(**validated_data)
        
        # 创建用户档案
        UserProfile.objects.create(user=user, **profile_data)
        
        return user

class PermissionLogSerializer(serializers.ModelSerializer):
    """权限日志序列化器"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    
    class Meta:
        model = PermissionLog
        fields = ['id', 'user', 'user_username', 'action', 'action_display', 'resource', 'permission', 
                 'group', 'ip_address', 'success', 'message', 'created_at']

class GroupPermissionSerializer(serializers.Serializer):
    """组权限管理序列化器"""
    group_id = serializers.IntegerField()
    permission_ids = serializers.ListField(child=serializers.IntegerField())

class UserGroupSerializer(serializers.Serializer):
    """用户组管理序列化器"""
    user_id = serializers.IntegerField()
    group_ids = serializers.ListField(child=serializers.IntegerField())

class UserPermissionSerializer(serializers.Serializer):
    """用户权限管理序列化器"""
    user_id = serializers.IntegerField()
    permission_ids = serializers.ListField(child=serializers.IntegerField())

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
