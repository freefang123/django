# 项目运行指南

## 🚀 快速启动

### 1. 激活虚拟环境
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 数据库迁移
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. 创建超级用户（可选）
```bash
python manage.py createsuperuser
```

### 5. 启动服务器
```bash
python manage.py runserver
```

## 📋 详细步骤

### 第一步：环境准备

#### 1.1 检查Python版本
```bash
python --version
# 确保Python版本 >= 3.8
```

#### 1.2 激活虚拟环境
```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

#### 1.3 升级pip
```bash
python -m pip install --upgrade pip
```

### 第二步：安装依赖

#### 2.1 基础依赖（推荐）
```bash
pip install -r requirements.txt
```

#### 2.2 开发环境依赖（可选）
```bash
pip install -r requirements-dev.txt
```

#### 2.3 生产环境依赖（可选）
```bash
pip install -r requirements-prod.txt
```

### 第三步：数据库配置

#### 3.1 确保MySQL服务运行
```bash
# Windows - 检查MySQL服务状态
net start mysql

# Linux/Mac
sudo systemctl status mysql
```

#### 3.2 创建数据库（如果不存在）
```sql
CREATE DATABASE test CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 3.3 数据库迁移
```bash
# 创建迁移文件
python manage.py makemigrations

# 应用迁移
python manage.py migrate
```

### 第四步：创建管理员账户

```bash
python manage.py createsuperuser
# 按提示输入用户名、邮箱和密码
```

### 第五步：启动服务器

#### 5.1 开发服务器
```bash
python manage.py runserver
```

#### 5.2 指定端口
```bash
python manage.py runserver 8000
```

#### 5.3 允许外部访问
```bash
python manage.py runserver 0.0.0.0:8000
```

## 🌐 访问地址

### 管理后台
- **地址**: http://localhost:8000/admin/
- **用途**: Django管理界面

### API文档
- **基础URL**: http://localhost:8000/api/
- **认证URL**: http://localhost:8000/api/auth/

### 主要API端点

#### 认证相关
```
POST /api/auth/register/     # 用户注册
POST /api/auth/login/        # 用户登录
GET  /api/auth/profile/      # 获取用户档案
PUT  /api/auth/profile/update/  # 更新用户档案
POST /api/auth/change-password/  # 修改密码
POST /api/auth/logout/       # 用户登出
POST /api/auth/refresh/      # 刷新令牌
```

#### JWT令牌
```
POST /api/token/            # 获取访问令牌
POST /api/token/refresh/    # 刷新访问令牌
```

#### 业务API
```
GET  /api/hello/           # 获取账户信息
GET  /api/ok/              # 简单响应
POST /api/multiprocessing/ # 多进程处理
POST /api/threading/       # 多线程处理
POST /api/encrypt/         # 数据加密
POST /api/decrypt/         # 数据解密
GET  /api/panda/           # Pandas数据处理
```

## 🧪 测试API

### 使用提供的测试脚本
```bash
python test_api.py
```

### 使用curl测试
```bash
# 测试基础API
curl http://localhost:8000/api/ok/

# 注册用户
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123","confirm_password":"testpass123","email":"test@example.com"}'

# 登录获取令牌
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}'
```

## 🔧 常见问题解决

### 1. 依赖安装失败
```bash
# 升级pip
python -m pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 2. MySQL连接错误
```bash
# 检查MySQL服务
net start mysql

# 检查数据库配置
python manage.py dbshell
```

### 3. 端口被占用
```bash
# 使用其他端口
python manage.py runserver 8001
```

### 4. 迁移错误
```bash
# 重置迁移
python manage.py migrate --fake-initial

# 重新创建迁移
python manage.py makemigrations --empty
```

### 5. 应用标签冲突
如果遇到 `Application labels aren't unique, duplicates: auth` 错误：
- 确保 `auth` 文件夹已重命名为 `auth_app`
- 检查 `settings.py` 中的 `INSTALLED_APPS` 配置
- 确保URL配置中的引用已更新

## 📊 项目结构

```
myproject/
├── api/          # API模块
├── auth_app/     # 认证模块（重命名避免冲突）
├── models/       # 数据模型
├── utils/        # 工具函数
├── services/     # 服务层
├── myproject/    # 主配置
├── templates/    # 模板文件
└── static/       # 静态文件
```

## ✅ 运行状态检查

### 检查服务器是否运行
```bash
# 测试基础API
curl http://localhost:8000/api/ok/

# 预期响应
{"success":true,"message":"ok, Django!","cit":null}
```

### 检查管理后台
- 访问 http://localhost:8000/admin/
- 使用创建的超级用户登录

## 🎯 下一步

1. **测试所有API端点**
2. **配置生产环境**
3. **添加更多功能**
4. **优化性能**

## 🎉 恭喜！

您的Django API项目已经成功运行！现在可以开始使用所有功能了。 