from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import MenuItem, MenuPermission, UserMenuLog
from django.contrib.auth.models import User, Group

@staff_member_required
def menu_tree_view(request):
    """菜单树管理视图"""
    # 获取菜单树数据
    root_menus = MenuItem.objects.filter(
        parent__isnull=True
    ).prefetch_related(
        Prefetch('menuitem_set', queryset=MenuItem.objects.filter(is_active=True).order_by('order'))
    ).order_by('order')
    
    # 获取统计信息
    total_menus = MenuItem.objects.count()
    active_menus = MenuItem.objects.filter(is_active=True).count()
    root_menus_count = MenuItem.objects.filter(parent__isnull=True).count()
    
    # 获取权限统计
    menu_permissions = MenuPermission.objects.select_related('menu', 'group', 'user')
    permission_stats = {
        'total_permissions': menu_permissions.count(),
        'group_permissions': menu_permissions.filter(group__isnull=False).count(),
        'user_permissions': menu_permissions.filter(user__isnull=False).count(),
    }
    
    context = {
        'title': '菜单树管理',
        'root_menus': root_menus,
        'stats': {
            'total_menus': total_menus,
            'active_menus': active_menus,
            'root_menus_count': root_menus_count,
            **permission_stats
        }
    }
    
    return render(request, 'admin/menu_tree.html', context)

def menu_tree_api(request):
    """菜单树API接口"""
    if request.method == 'GET':
        # 获取菜单树数据
        root_menus = MenuItem.objects.filter(
            parent__isnull=True
        ).prefetch_related(
            Prefetch('menuitem_set', queryset=MenuItem.objects.filter(is_active=True).order_by('order'))
        ).order_by('order')
        
        def build_tree_data(menus):
            tree_data = []
            for menu in menus:
                menu_data = {
                    'id': menu.id,
                    'title': menu.title,
                    'name': menu.name,
                    'icon': menu.icon,
                    'url': menu.url,
                    'component': menu.component,
                    'menu_type': menu.menu_type,
                    'order': menu.order,
                    'is_active': menu.is_active,
                    'description': menu.description,
                    'children': build_tree_data(menu.menuitem_set.all()) if menu.menuitem_set.exists() else []
                }
                tree_data.append(menu_data)
            return tree_data
        
        tree_data = build_tree_data(root_menus)
        
        return JsonResponse({
            'success': True,
            'data': tree_data
        })
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)

@staff_member_required
def menu_permissions_view(request):
    """菜单权限管理视图"""
    # 获取菜单权限数据
    menu_permissions = MenuPermission.objects.select_related('menu', 'group', 'user')
    
    # 获取用户和组数据
    users = User.objects.all()
    groups = Group.objects.all()
    menus = MenuItem.objects.all()
    
    context = {
        'title': '菜单权限管理',
        'menu_permissions': menu_permissions,
        'users': users,
        'groups': groups,
        'menus': menus
    }
    
    return render(request, 'admin/menu_permissions.html', context)

@staff_member_required
def menu_logs_view(request):
    """菜单访问日志视图"""
    # 获取菜单访问日志
    logs = UserMenuLog.objects.select_related('user', 'menu').order_by('-created_at')
    
    # 获取统计信息
    total_logs = logs.count()
    unique_users = logs.values('user').distinct().count()
    unique_menus = logs.values('menu').distinct().count()
    
    context = {
        'title': '菜单访问日志',
        'logs': logs,
        'stats': {
            'total_logs': total_logs,
            'unique_users': unique_users,
            'unique_menus': unique_menus
        }
    }
    
    return render(request, 'admin/menu_logs.html', context)
