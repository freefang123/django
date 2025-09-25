# 项目安装和配置文档

本文件夹包含项目安装、配置和运行相关的所有文档。

## 文档列表

- `INSTALL.md` - 项目安装说明
- `RUN_GUIDE.md` - 项目运行指南
- `QUICK_START.md` - 快速开始指南
- `DATABASE_CONFIG.md` - 数据库配置说明
- `PROJECT_STRUCTURE.md` - 项目结构说明
- `JWT_FIX_COMPLETE.md` - JWT认证修复完成说明

## 使用指南

### 新用户
1. 首先阅读 `QUICK_START.md` 了解项目概况
2. 按照 `INSTALL.md` 进行环境安装
3. 参考 `RUN_GUIDE.md` 启动项目
4. 查看 `PROJECT_STRUCTURE.md` 了解项目结构

### 开发者
1. 查看 `PROJECT_STRUCTURE.md` 了解代码组织
2. 参考 `DATABASE_CONFIG.md` 配置数据库
3. 查看 `JWT_FIX_COMPLETE.md` 了解认证系统

## 环境要求

- Python 3.8+
- Django 4.0+
- SQLite/PostgreSQL/MySQL
- 其他依赖见 `requirements.txt`

## 快速开始

```bash
# 1. 克隆项目
git clone <repository-url>

# 2. 安装依赖
pip install -r requirements.txt

# 3. 数据库迁移
python manage.py migrate

# 4. 创建超级用户
python manage.py createsuperuser

# 5. 启动服务器
python manage.py runserver
```
