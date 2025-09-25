from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import render
from .models import UserProfile, PermissionLog, MenuItem, MenuPermission, UserMenuLog
from .serializers import (
    UserSerializer, UserCreateSerializer, UserProfileSerializer,
    GroupSerializer, PermissionSerializer, PermissionLogSerializer,
    GroupPermissionSerializer, UserGroupSerializer, UserPermissionSerializer,
    MenuItemSerializer, MenuPermissionSerializer, UserMenuLogSerializer,
    MenuTreeSerializer, UserMenuSerializer, GroupMenuSerializer
)
from utils.permission_utils import log_permission_action, get_client_ip

def permission_admin_view(request):
    """权限管理页面视图"""
    return render(request, 'permission_admin.html')

class UserListView(generics.ListCreateAPIView):
    """用户列表视图"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = User.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) |
                Q(email__icontains=search) |
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search)
            )
        return queryset

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情视图"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class UserCreateView(generics.CreateAPIView):
    """用户创建视图"""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GroupListView(generics.ListCreateAPIView):
    """组列表视图"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    """组详情视图"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class PermissionListView(generics.ListAPIView):
    """权限列表视图"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = Permission.objects.all()
        content_type = self.request.query_params.get('content_type', None)
        if content_type:
            queryset = queryset.filter(content_type__model=content_type)
        return queryset

class PermissionLogListView(generics.ListAPIView):
    """权限日志列表视图"""
    queryset = PermissionLog.objects.all()
    serializer_class = PermissionLogSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = PermissionLog.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        action = self.request.query_params.get('action', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if action:
            queryset = queryset.filter(action=action)
        return queryset

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def assign_group_permissions(request):
    """分配组权限"""
    serializer = GroupPermissionSerializer(data=request.data)
    if serializer.is_valid():
        group_id = serializer.validated_data['group_id']
        permission_ids = serializer.validated_data['permission_ids']
        
        try:
            group = Group.objects.get(id=group_id)
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
            
            log_permission_action(
                request.user,
                'permission_granted',
                f'Group: {group.name}',
                f'Permissions: {permission_ids}',
                True,
                f'为组 {group.name} 分配权限',
                request
            )
            
            return Response({
                'success': True,
                'message': f'成功为组 {group.name} 分配权限'
            }, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({
                'success': False,
                'message': '组不存在'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'message': '数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def assign_user_groups(request):
    """分配用户组"""
    serializer = UserGroupSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        group_ids = serializer.validated_data['group_ids']
        
        try:
            user = User.objects.get(id=user_id)
            groups = Group.objects.filter(id__in=group_ids)
            user.groups.set(groups)
            
            group_names = [group.name for group in groups]
            log_permission_action(
                request.user,
                'group_added',
                f'User: {user.username}',
                f'Groups: {group_names}',
                True,
                f'为用户 {user.username} 分配组',
                request
            )
            
            return Response({
                'success': True,
                'message': f'成功为用户 {user.username} 分配组'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'message': '数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def assign_user_permissions(request):
    """分配用户权限"""
    serializer = UserPermissionSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        permission_ids = serializer.validated_data['permission_ids']
        
        try:
            user = User.objects.get(id=user_id)
            permissions = Permission.objects.filter(id__in=permission_ids)
            user.user_permissions.set(permissions)
            
            log_permission_action(
                request.user,
                'permission_granted',
                f'User: {user.username}',
                f'Permissions: {permission_ids}',
                True,
                f'为用户 {user.username} 分配权限',
                request
            )
            
            return Response({
                'success': True,
                'message': f'成功为用户 {user.username} 分配权限'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'message': '数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_permissions(request):
    """获取当前用户权限"""
    user = request.user
    permissions = user.get_all_permissions()
    groups = user.groups.all()
    
    return Response({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        },
        'permissions': list(permissions),
        'groups': [{'id': group.id, 'name': group.name} for group in groups]
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def permission_stats(request):
    """权限统计信息"""
    total_users = User.objects.count()
    total_groups = Group.objects.count()
    total_permissions = Permission.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    return Response({
        'success': True,
        'stats': {
            'total_users': total_users,
            'active_users': active_users,
            'total_groups': total_groups,
            'total_permissions': total_permissions,
        }
    }, status=status.HTTP_200_OK)

# 菜单相关视图
class MenuItemListView(generics.ListCreateAPIView):
    """菜单项列表视图"""
    queryset = MenuItem.objects.filter(parent__isnull=True, is_active=True)
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def get_queryset(self):
        queryset = MenuItem.objects.filter(parent__isnull=True, is_active=True)
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(title__icontains=search)
            )
        return queryset.order_by('order')

class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """菜单项详情视图"""
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class MenuTreeView(generics.ListAPIView):
    """菜单树视图"""
    queryset = MenuItem.objects.filter(parent__isnull=True, is_active=True)
    serializer_class = MenuTreeSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_menu_view(request):
    """获取当前用户菜单"""
    user = request.user
    
    # 记录菜单访问日志
    log_permission_action(
        user,
        'menu_access',
        'user_menu',
        None,
        True,
        '用户访问菜单',
        request
    )
    
    # 获取用户有权限的菜单
    user_menus = get_user_menus(user)
    
    return Response({
        'success': True,
        'menus': user_menus,
        'user': {
            'id': user.id,
            'username': user.username,
            'is_superuser': user.is_superuser,
            'is_staff': user.is_staff,
        }
    }, status=status.HTTP_200_OK)

def get_user_menus(user):
    """获取用户菜单"""
    # 如果是超级用户，返回所有菜单
    if user.is_superuser:
        return get_all_menus()
    
    # 获取用户有权限的菜单
    menu_permissions = MenuPermission.objects.filter(
        Q(user=user) | Q(group__in=user.groups.all()) | Q(permission__in=user.get_all_permissions()),
        is_active=True
    ).select_related('menu', 'menu__parent')
    
    # 获取菜单ID列表
    menu_ids = set()
    for mp in menu_permissions:
        menu_ids.add(mp.menu.id)
        # 添加父菜单
        if mp.menu.parent:
            menu_ids.add(mp.menu.parent.id)
    
    # 获取菜单树
    menus = MenuItem.objects.filter(
        id__in=menu_ids,
        is_active=True
    ).order_by('order')
    
    return build_menu_tree(menus)

def get_all_menus():
    """获取所有菜单"""
    menus = MenuItem.objects.filter(is_active=True).order_by('order')
    return build_menu_tree(menus)

def build_menu_tree(menus):
    """构建菜单树"""
    menu_dict = {}
    root_menus = []
    
    # 创建菜单字典
    for menu in menus:
        menu_dict[menu.id] = {
            'id': menu.id,
            'name': menu.name,
            'title': menu.title,
            'icon': menu.icon,
            'url': menu.url,
            'component': menu.component,
            'menu_type': menu.menu_type,
            'order': menu.order,
            'children': []
        }
    
    # 构建树结构
    for menu in menus:
        menu_data = menu_dict[menu.id]
        if menu.parent:
            if menu.parent.id in menu_dict:
                menu_dict[menu.parent.id]['children'].append(menu_data)
        else:
            root_menus.append(menu_data)
    
    return root_menus

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def assign_user_menus(request):
    """分配用户菜单"""
    serializer = UserMenuSerializer(data=request.data)
    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        menu_ids = serializer.validated_data['menu_ids']
        
        try:
            user = User.objects.get(id=user_id)
            menus = MenuItem.objects.filter(id__in=menu_ids)
            
            # 清除现有权限
            MenuPermission.objects.filter(user=user).delete()
            
            # 分配新权限
            for menu in menus:
                MenuPermission.objects.create(
                    menu=menu,
                    user=user,
                    is_active=True
                )
            
            log_permission_action(
                request.user,
                'menu_permission_granted',
                f'User: {user.username}',
                f'Menus: {menu_ids}',
                True,
                f'为用户 {user.username} 分配菜单权限',
                request
            )
            
            return Response({
                'success': True,
                'message': f'成功为用户 {user.username} 分配菜单权限'
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'message': '用户不存在'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'message': '数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def assign_group_menus(request):
    """分配组菜单"""
    serializer = GroupMenuSerializer(data=request.data)
    if serializer.is_valid():
        group_id = serializer.validated_data['group_id']
        menu_ids = serializer.validated_data['menu_ids']
        
        try:
            group = Group.objects.get(id=group_id)
            menus = MenuItem.objects.filter(id__in=menu_ids)
            
            # 清除现有权限
            MenuPermission.objects.filter(group=group).delete()
            
            # 分配新权限
            for menu in menus:
                MenuPermission.objects.create(
                    menu=menu,
                    group=group,
                    is_active=True
                )
            
            log_permission_action(
                request.user,
                'menu_permission_granted',
                f'Group: {group.name}',
                f'Menus: {menu_ids}',
                True,
                f'为组 {group.name} 分配菜单权限',
                request
            )
            
            return Response({
                'success': True,
                'message': f'成功为组 {group.name} 分配菜单权限'
            }, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({
                'success': False,
                'message': '组不存在'
            }, status=status.HTTP_404_NOT_FOUND)
    
    return Response({
        'success': False,
        'message': '数据验证失败',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu_permissions(request):
    """获取菜单权限列表"""
    menu_permissions = MenuPermission.objects.all().select_related('menu', 'group', 'user')
    serializer = MenuPermissionSerializer(menu_permissions, many=True)
    
    return Response({
        'success': True,
        'permissions': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def menu_logs(request):
    """获取菜单访问日志"""
    logs = UserMenuLog.objects.all().select_related('user', 'menu')
    serializer = UserMenuLogSerializer(logs, many=True)
    
    return Response({
        'success': True,
        'logs': serializer.data
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def log_menu_access(request):
    """记录菜单访问日志"""
    menu_id = request.data.get('menu_id')
    action = request.data.get('action', 'access')
    
    try:
        menu = MenuItem.objects.get(id=menu_id)
        
        # 记录访问日志
        UserMenuLog.objects.create(
            user=request.user,
            menu=menu,
            action=action,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'success': True,
            'message': '菜单访问日志记录成功'
        }, status=status.HTTP_200_OK)
    except MenuItem.DoesNotExist:
        return Response({
            'success': False,
            'message': '菜单不存在'
        }, status=status.HTTP_404_NOT_FOUND)