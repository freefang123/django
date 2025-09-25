from django.urls import path
from . import views

urlpatterns = [
    # 认证相关API
    path('login', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.user_profile_view, name='profile'),
    path('profile/update', views.update_profile_view, name='update_profile'),
    path('change-password', views.change_password_view, name='change_password'),
    path('refresh', views.refresh_token_view, name='refresh_token'),
] 