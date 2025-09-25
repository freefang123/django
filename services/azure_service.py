from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import pandas as pd
import pytz
from io import BytesIO

class AzureBlobService:
    """Azure Blob存储服务"""
    
    def __init__(self, connection_string, container_name="test"):
        """
        初始化Azure Blob服务
        
        Args:
            connection_string (str): Azure连接字符串
            container_name (str): 容器名称
        """
        self.connection_string = connection_string
        self.container_name = container_name
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.blob_service_client.get_container_client(container_name)
    
    def log_request(self, ip, phone_number):
        """
        记录请求日志到Azure Blob
        
        Args:
            ip (str): IP地址
            phone_number (str): 电话号码
            
        Returns:
            str: 操作结果
        """
        now = datetime.now(pytz.timezone('Asia/Shanghai'))
        today = now.strftime('%Y-%m-%d')
        blob_client = self.container_client.get_blob_client(blob=f"app_logs_{today}.xlsx")

        log_data = [
            {"IP": ip, "Phone": phone_number, "Time": now.strftime('%Y-%m-%d %H:%M:%S')},
            {"IP": ip, "Phone": phone_number, "Time": now.strftime('%Y-%m-%d %H:%M:%S')},
            {"IP": ip, "Phone": phone_number, "Time": now.strftime('%Y-%m-%d %H:%M:%S')}
        ]

        df = pd.DataFrame(log_data)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)

        blob_client.upload_blob(output, overwrite=True)
        return "ok"
    
    def generate_url_token(self, account_key, account_name, blob_name="app_logs_2024-07-04.xlsx"):
        """
        生成Azure Blob访问令牌
        
        Args:
            account_key (str): 账户密钥
            account_name (str): 账户名称
            blob_name (str): Blob名称
            
        Returns:
            str: 访问令牌
        """
        account_url = f"https://{account_name}.blob.core.chinacloudapi.cn/"
        
        client = BlobServiceClient(account_url=account_url, credential=account_key)
        permission = BlobSasPermissions(read=True, write=True, delete=True)
        token = generate_blob_sas(
            account_name=account_name,
            account_key=account_key,
            container_name=self.container_name,
            blob_name=blob_name,
            permission=permission,
            expiry=datetime.utcnow() + timedelta(hours=30*24),
        )

        return token
    
    def get_blob_url(self, account_key, account_name, blob_name="app_logs_2024-07-04.json"):
        """
        获取Blob下载链接
        
        Args:
            account_key (str): 账户密钥
            account_name (str): 账户名称
            blob_name (str): Blob名称
            
        Returns:
            str: Blob下载链接
        """
        sas_token = self.generate_url_token(account_key, account_name, blob_name)
        blob_url = f"https://{account_name}.blob.core.chinacloudapi.cn/{self.container_name}/{blob_name}?{sas_token}"
        return blob_url 