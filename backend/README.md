# 文档管理系统 - 后端

基于 FastAPI 的文档管理系统后端 API。

## 项目结构

```
backend/
├── app/
│   ├── api/              # API 路由层
│   │   └── v1/           # API v1 版本
│   ├── core/             # 核心配置和工具
│   │   ├── config.py    # 应用配置
│   │   ├── database.py  # 数据库配置
│   │   ├── exceptions.py # 异常定义
│   │   └── dependencies.py # 依赖注入
│   ├── models/           # 数据模型
│   ├── repositories/     # 数据访问层
│   ├── schemas/          # Pydantic 模式
│   ├── services/         # 业务逻辑层
│   └── main.py          # 应用入口
├── requirements.txt     # Python 依赖
└── .env.example         # 环境变量示例
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

或者使用启动脚本：

```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

### 4. 访问 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 端点

- `GET /` - 根路径
- `GET /health` - 健康检查
- `POST /api/v1/documents/upload` - 上传文档
- `GET /api/v1/documents/` - 获取文档列表
- `GET /api/v1/documents/{id}` - 获取文档详情
- `GET /api/v1/documents/{id}/download` - 下载文档
- `PUT /api/v1/documents/{id}` - 更新文档
- `DELETE /api/v1/documents/{id}` - 删除文档
- `GET /api/v1/tags/` - 获取标签列表
- `POST /api/v1/tags/` - 创建标签
- `GET /api/v1/search/` - 搜索文档
- `POST /api/v1/pdf/generate` - 生成 PDF 汇编

## 架构说明

### 分层架构

1. **API 层** (`app/api/`): 处理 HTTP 请求和响应
2. **服务层** (`app/services/`): 业务逻辑处理
3. **仓库层** (`app/repositories/`): 数据访问抽象
4. **模型层** (`app/models/`): 数据库模型定义

### 设计模式

- **依赖注入**: 使用 FastAPI 的 Depends
- **仓库模式**: 数据访问层抽象
- **服务层模式**: 业务逻辑封装

