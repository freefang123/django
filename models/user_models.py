from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    """账户模型"""
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    class Meta:
        db_table = 'myproject_account'  # 指定表名
        verbose_name = "账户"
        verbose_name_plural = "账户"

class UserProfile(models.Model):
    """用户档案模型"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    class Meta:
        db_table = 'myproject_userprofile'  # 指定表名
        verbose_name = "用户档案"
        verbose_name_plural = "用户档案" 