#!/usr/bin/env python
"""
测试分页类导入
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

try:
    import django
    django.setup()
    
    from chat_app.views import ChatMessagePagination
    print("✅ ChatMessagePagination 导入成功")
    
    # 测试分页类
    pagination = ChatMessagePagination()
    print(f"✅ 分页类创建成功")
    print(f"  - page_size: {pagination.page_size}")
    print(f"  - page_size_query_param: {pagination.page_size_query_param}")
    print(f"  - max_page_size: {pagination.max_page_size}")
    print(f"  - page_query_param: {pagination.page_query_param}")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()
