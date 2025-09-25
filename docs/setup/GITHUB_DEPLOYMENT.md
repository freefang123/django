# GitHub 部署指南

本指南将帮助您将项目发布到 GitHub。

## 准备工作

### 1. 检查 .gitignore 文件
确保 `.gitignore` 文件已正确配置，忽略以下文件：
- 虚拟环境文件夹 (`venv/`)
- 数据库文件 (`db.sqlite3`)
- Python 缓存文件 (`__pycache__/`)
- 日志文件 (`*.log`)
- IDE 配置文件 (`.vscode/`, `.idea/`)

### 2. 检查敏感信息
确保以下文件不包含敏感信息：
- 数据库密码
- API 密钥
- 管理员密码
- 其他机密信息

## 发布步骤

### 1. 初始化 Git 仓库（如果尚未初始化）
```bash
git init
```

### 2. 添加所有文件到暂存区
```bash
git add .
```

### 3. 提交代码
```bash
git commit -m "Initial commit: Django权限管理系统"
```

### 4. 创建 GitHub 仓库
1. 登录 GitHub
2. 点击 "New repository"
3. 输入仓库名称（如：django-permission-system）
4. 选择 "Public" 或 "Private"
5. 不要勾选 "Initialize this repository with a README"

### 5. 添加远程仓库
```bash
git remote add origin https://github.com/yourusername/your-repo-name.git
```

### 6. 推送到 GitHub
```bash
git push -u origin master
```

## 项目结构说明

```
django-permission-system/
├── docs/                    # 项目文档
│   ├── api/                # API文档
│   ├── menu/               # 菜单系统文档
│   ├── permission/         # 权限管理文档
│   └── setup/              # 安装配置文档
├── tests/                  # 测试文件
├── permission_app/         # 权限管理应用
├── auth_app/               # 认证应用
├── api/                    # API接口
├── models/                 # 数据模型
├── services/               # 服务层
├── utils/                  # 工具函数
├── templates/              # 模板文件
├── static/                 # 静态文件
├── requirements.txt        # 依赖包
└── manage.py              # Django管理脚本
```

## 部署到生产环境

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/your-repo-name.git
cd your-repo-name
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 创建 .env 文件
cp .env.example .env
# 编辑 .env 文件，设置数据库配置等
```

### 4. 数据库迁移
```bash
python manage.py migrate
```

### 5. 创建超级用户
```bash
python manage.py createsuperuser
```

### 6. 启动服务器
```bash
python manage.py runserver
```

## 注意事项

1. **不要提交敏感信息**：确保 `.env` 文件、数据库文件等敏感信息不被提交
2. **使用环境变量**：在生产环境中使用环境变量存储敏感配置
3. **定期备份**：定期备份数据库和重要文件
4. **更新依赖**：定期更新依赖包以修复安全漏洞

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 许可证

本项目使用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
