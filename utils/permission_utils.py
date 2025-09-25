from functools import wraps
from django.http import JsonResponse
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework import status
from permission_app.models import PermissionLog
import logging

logger = logging.getLogger(__name__)

def get_client_ip(request):
    """获取客户端IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def log_permission_action(user, action, resource, permission=None, success=True, message=None, request=None):
    """记录权限操作日志"""
    try:
        ip_address = get_client_ip(request) if request else '127.0.0.1'
        user_agent = request.META.get('HTTP_USER_AGENT', '') if request else ''
        
        PermissionLog.objects.create(
            user=user,
            action=action,
            resource=resource,
            permission=permission,
            ip_address=ip_address,
            user_agent=user_agent,
            success=success,
            message=message
        )
    except Exception as e:
        logger.error(f"记录权限日志失败: {str(e)}")

def has_permission(user, permission_codename):
    """检查用户是否有特定权限"""
    if not user or not user.is_authenticated:
        return False
    
    return user.has_perm(permission_codename)

def has_any_permission(user, permission_codenames):
    """检查用户是否有任意一个权限"""
    if not user or not user.is_authenticated:
        return False
    
    for permission in permission_codenames:
        if user.has_perm(permission):
            return True
    return False

def has_group(user, group_name):
    """检查用户是否属于特定组"""
    if not user or not user.is_authenticated:
        return False
    
    return user.groups.filter(name=group_name).exists()

def has_any_group(user, group_names):
    """检查用户是否属于任意一个组"""
    if not user or not user.is_authenticated:
        return False
    
    return user.groups.filter(name__in=group_names).exists()

def require_permission(permission_codename):
    """权限装饰器"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                log_permission_action(
                    request.user, 
                    'access_denied', 
                    request.path, 
                    permission_codename, 
                    False, 
                    '用户未认证',
                    request
                )
                return JsonResponse({
                    'success': False,
                    'message': '需要登录才能访问此资源'
                }, status=401)
            
            if not has_permission(request.user, permission_codename):
                log_permission_action(
                    request.user, 
                    'access_denied', 
                    request.path, 
                    permission_codename, 
                    False, 
                    f'用户缺少权限: {permission_codename}',
                    request
                )
                return JsonResponse({
                    'success': False,
                    'message': f'您没有权限访问此资源，需要权限: {permission_codename}'
                }, status=403)
            
            log_permission_action(
                request.user, 
                'access_granted', 
                request.path, 
                permission_codename, 
                True, 
                '权限验证通过',
                request
            )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_group(group_name):
    """组装饰器"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                log_permission_action(
                    request.user, 
                    'access_denied', 
                    request.path, 
                    group_name, 
                    False, 
                    '用户未认证',
                    request
                )
                return JsonResponse({
                    'success': False,
                    'message': '需要登录才能访问此资源'
                }, status=401)
            
            if not has_group(request.user, group_name):
                log_permission_action(
                    request.user, 
                    'access_denied', 
                    request.path, 
                    group_name, 
                    False, 
                    f'用户缺少组权限: {group_name}',
                    request
                )
                return JsonResponse({
                    'success': False,
                    'message': f'您没有权限访问此资源，需要组: {group_name}'
                }, status=403)
            
            log_permission_action(
                request.user, 
                'access_granted', 
                request.path, 
                group_name, 
                True, 
                '组权限验证通过',
                request
            )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_any_group(*group_names):
    """任意组装饰器"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                log_permission_action(
                    request.user, 
                    'access_denied', 
                    request.path, 
                    ', '.join(group_names), 
                    False, 
                    '用户未认证',
                    request
                )
                return JsonResponse({
                    'success': False,
                    'message': '需要登录才能访问此资源'
                }, status=401)
            
            if not has_any_group(request.user, group_names):
                log_permission_action(
                    request.user, 
                    'access_denied', 
                    request.path, 
                    ', '.join(group_names), 
                    False, 
                    f'用户缺少组权限: {", ".join(group_names)}',
                    request
                )
                return JsonResponse({
                    'success': False,
                    'message': f'您没有权限访问此资源，需要以下组之一: {", ".join(group_names)}'
                }, status=403)
            
            log_permission_action(
                request.user, 
                'access_granted', 
                request.path, 
                ', '.join(group_names), 
                True, 
                '组权限验证通过',
                request
            )
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def require_superuser(view_func):
    """超级用户装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            log_permission_action(
                request.user, 
                'access_denied', 
                request.path, 
                'superuser', 
                False, 
                '用户未认证',
                request
            )
            return JsonResponse({
                'success': False,
                'message': '需要登录才能访问此资源'
            }, status=401)
        
        if not request.user.is_superuser:
            log_permission_action(
                request.user, 
                'access_denied', 
                request.path, 
                'superuser', 
                False, 
                '用户不是超级用户',
                request
            )
            return JsonResponse({
                'success': False,
                'message': '您没有权限访问此资源，需要超级用户权限'
            }, status=403)
        
        log_permission_action(
            request.user, 
            'access_granted', 
            request.path, 
            'superuser', 
            True, 
            '超级用户权限验证通过',
            request
        )
        
        return view_func(request, *args, **kwargs)
    return wrapper

def require_staff(view_func):
    """员工装饰器"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            log_permission_action(
                request.user, 
                'access_denied', 
                request.path, 
                'staff', 
                False, 
                '用户未认证',
                request
            )
            return JsonResponse({
                'success': False,
                'message': '需要登录才能访问此资源'
            }, status=401)
        
        if not request.user.is_staff:
            log_permission_action(
                request.user, 
                'access_denied', 
                request.path, 
                'staff', 
                False, 
                '用户不是员工',
                request
            )
            return JsonResponse({
                'success': False,
                'message': '您没有权限访问此资源，需要员工权限'
            }, status=403)
        
        log_permission_action(
            request.user, 
            'access_granted', 
            request.path, 
            'staff', 
            True, 
            '员工权限验证通过',
            request
        )
        
        return view_func(request, *args, **kwargs)
    return wrapper
