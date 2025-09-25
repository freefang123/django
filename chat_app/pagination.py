"""
聊天应用分页配置
"""
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ChatMessagePagination(PageNumberPagination):
    """聊天消息分页类"""
    page_size = 50  # 默认每页50条
    page_size_query_param = 'page_size'  # 允许客户端指定每页大小
    max_page_size = 100  # 最大每页100条
    page_query_param = 'page'  # 页码参数名
    
    def get_paginated_response(self, data):
        """自定义分页响应格式"""
        return Response({
            'results': data,
            'pagination': {
                'current_page': self.page.number,
                'total_pages': self.page.paginator.num_pages,
                'page_size': self.page.paginator.per_page,
                'total_count': self.page.paginator.count,
                'has_next': self.page.has_next(),
                'has_previous': self.page.has_previous(),
                'next_page': self.page.next_page_number() if self.page.has_next() else None,
                'previous_page': self.page.previous_page_number() if self.page.has_previous() else None,
            }
        })
