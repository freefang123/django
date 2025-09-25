from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from django.db.models import Q
from .menu_models import MenuItem, MenuPermission, UserMenuLog
from .menu_serializers import (
    MenuItemSerializer, MenuPermissionSerializer, UserMenuLogSerializer,
    MenuTreeSerializer, UserMenuSerializer, GroupMenuSerializer
)
from utils.permission_utils import log_permission_action, get_client_ip

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
    ).select_related('menu')
    
    # 获取菜单ID列表
    menu_ids = set()
    for mp in menu_permissions:
        menu_ids.add(mp.menu.id)
        # 添加父菜单
        parent = mp.menu.parent
        while parent:
            menu_ids.add(parent.id)
            parent = parent.parent
    
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
