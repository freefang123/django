import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from models.user_models import Account
from auth_app.serializers import AccountSerializer
from utils.crypto_utils import encrypt_data, decrypt_data
from utils.process_utils import run_multiprocessing_task, run_multithreading_task
from utils.permission_utils import require_permission, require_group, require_superuser
from services.data_service import DataProcessingService

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accounts_api(request):
    """
    获取所有账户信息API（需要登录）
    GET /api/accounts/
    
    请求头需要包含：
    Authorization: Bearer <your_jwt_token>
    """
    try:
        # 获取所有账户信息
        accounts = Account.objects.all()
        
        # 使用序列化器
        serializer = AccountSerializer(accounts, many=True)
        
        return Response({
            'success': True,
            'message': '获取所有账户信息成功',
            'data': serializer.data,
            'count': len(serializer.data)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': f'获取账户信息失败: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_permission('api.add_account')
def multiprocessing_api(request):
    """
    多进程处理API
    POST /api/multiprocessing/
    """
    try:
        results = run_multiprocessing_task()
        return Response({
            'success': True,
            'data': results
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@require_group('developers')
def threading_api(request):
    """
    多线程处理API
    POST /api/threading/
    """
    try:
        results = run_multithreading_task()
        return Response({
            'success': True,
            'data': results
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def encrypt_api(request):
    """
    数据加密API
    POST /api/encrypt/
    {
        "phone": "your_phone_number"
    }
    """
    try:
        phone = request.data.get("phone")
        if not phone:
            return Response({
                'success': False,
                'message': 'Phone number is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = encrypt_data(phone, os.getenv('ENCRYPTION_KEY', 'default_key'))
        
        return Response({
            'success': True,
            'data': results
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decrypt_api(request):
    """
    数据解密API
    POST /api/decrypt/
    {
        "asm": "encrypted_data"
    }
    """
    try:
        asm = request.data.get("asm")
        if not asm:
            return Response({
                'success': False,
                'message': 'Encrypted data is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        results = decrypt_data(asm, os.getenv('DECRYPTION_KEY', 'default_key'))
        
        return Response({
            'success': True,
            'data': results
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def panda_api(request):
    """
    Pandas数据处理API
    GET /api/panda/
    """
    try:
        result = DataProcessingService.process_student_data()
        
        return Response({
            'success': True,
            **result
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 