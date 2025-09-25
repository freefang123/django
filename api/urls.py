from django.urls import path
from . import views

urlpatterns = [
    # 基础API
    path('hello/', views.hello_api, name='hello_api'),
    path('ok/', views.ok_api, name='ok_api'),
    
    # 需要认证的API
    path('accounts/', views.accounts_api, name='accounts_api'),
    path('multiprocessing/', views.multiprocessing_api, name='multiprocessing_api'),
    path('threading/', views.threading_api, name='threading_api'),
    path('blob/', views.blob_api, name='blob_api'),
    path('blob-url/', views.blob_url_api, name='blob_url_api'),
    path('encrypt/', views.encrypt_api, name='encrypt_api'),
    path('decrypt/', views.decrypt_api, name='decrypt_api'),
    path('panda/', views.panda_api, name='panda_api'),
] 