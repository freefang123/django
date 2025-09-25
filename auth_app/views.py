from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import (
    LoginSerializer, 
    RegisterSerializer, 
    UserSerializer, 
    UserProfileSerializer,
    ChangePasswordSerializer
)
from models.user_models import UserProfile

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """
    用户登录API
    POST /api/auth/login
    {
        "username": "your_username",
        "password": "your_password"
    }
    """
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        
        # 获取或创建用户档案
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'success': True,
            'message': 'Login successful',
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)
    
    return Response({
        'success': False,
        'message': 'Login failed',
        'errors': serializer.errors
    }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """
    用户注册API
    POST /api/auth/register
    {
        "username": "new_user",
        "email": "user@example.com",
        "password": "password123",
        "confirm_password": "password123",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        # 创建用户档案
        profile = UserProfile.objects.create(user=user)
        
        return Response({
            'success': True,
            'message': 'Registration successful',
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            },
            'user': UserSerializer(user).data,
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_201_CREATED)
    
    return Response({
        'success': False,
        'message': 'Registration failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    用户登出API
    POST /api/auth/logout
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
        
        return Response({
            'success': True,
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Logout failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    """
    获取用户档案API
    GET /api/auth/profile
    """
    try:
        profile = request.user.profile
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data,
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        # 如果用户档案不存在，创建一个
        profile = UserProfile.objects.create(user=request.user)
        return Response({
            'success': True,
            'user': UserSerializer(request.user).data,
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    """
    更新用户档案API
    PUT /api/auth/profile/update
    {
        "phone": "1234567890",
        "avatar": "https://example.com/avatar.jpg"
    }
    """
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully',
                'profile': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            'success': False,
            'message': 'Profile update failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response({
            'success': False,
            'message': 'Profile not found'
        }, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    """
    修改密码API
    POST /api/auth/change-password
    {
        "old_password": "old_password",
        "new_password": "new_password",
        "confirm_password": "new_password"
    }
    """
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        if user.check_password(serializer.validated_data['old_password']):
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'success': True,
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Old password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({
        'success': False,
        'message': 'Password change failed',
        'errors': serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token_view(request):
    """
    刷新访问令牌API
    POST /api/auth/refresh
    {
        "refresh": "your_refresh_token"
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            refresh = RefreshToken(refresh_token)
            return Response({
                'success': True,
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'success': False,
                'message': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'success': False,
            'message': 'Token refresh failed',
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST) 