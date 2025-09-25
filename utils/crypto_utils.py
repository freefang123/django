import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

def encrypt_data(data, key):
    """
    使用AES加密数据
    
    Args:
        data (str): 要加密的数据
        key (str): 加密密钥
        
    Returns:
        str: 加密后的数据（格式：iv:encrypted_data）
    """
    # 转换密钥为字节
    key = key.encode('utf-8')
    
    # 初始化向量
    iv = b'1234567890123456'
    
    # 创建AES加密对象
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 加密数据
    ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    
    # 编码为base64
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    
    return iv + ':' + ct

def decrypt_data(encrypted_data, key):
    """
    使用AES解密数据
    
    Args:
        encrypted_data (str): 加密的数据（格式：iv:encrypted_data）
        key (str): 解密密钥
        
    Returns:
        str: 解密后的数据
    """
    # 转换密钥为字节
    key = key.encode('utf-8')
    
    # 分离IV和加密数据
    iv, ct = encrypted_data.split(':')
    
    # 解码base64
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    
    # 创建AES解密对象
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # 解密数据
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    
    return pt 