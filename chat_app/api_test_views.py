from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group


@login_required
def api_test_page(request):
    """API测试页面"""
    # 检查用户是否为developer
    is_developer = request.user.groups.filter(name='developer').exists()
    
    return render(request, 'api_test.html', {
        'is_developer': is_developer,
        'user': request.user
    })
