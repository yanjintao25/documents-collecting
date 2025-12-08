# 文档管理系统

一个基于 Vue3 + FastAPI + SQLite 的文档管理系统，支持文档上传、下载、标签管理、搜索和 PDF 汇编生成。

## 功能特性

- ✅ **文档上传**：支持多种格式文档上传
- ✅ **文档下载**：快速下载已上传的文档
- ✅ **标签管理**：为文档添加标签，方便分类管理
- ✅ **文档搜索**：支持关键词搜索和标签筛选
- ✅ **PDF 汇编**：选择多个 PDF 文档，生成汇编 PDF 文件
- ✅ **文档编辑**：修改文档描述和标签

## 技术栈

### 前端
- **Vue 3** + **TypeScript** - 渐进式 JavaScript 框架
- **Vite** - 下一代前端构建工具
- **Vue Router** - 官方路由管理器
- **Pinia** - 状态管理库
- **Element Plus** - Vue 3 组件库
- **Axios** - HTTP 客户端

### 后端
- **Python** + **FastAPI** - 现代、快速的 Web 框架
- **SQLAlchemy** - ORM 框架
- **SQLite** - 轻量级数据库
- **PyPDF2** - PDF 处理库

## 项目结构

```
documents-collecting/
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由层
│   │   │   └── v1/        # API v1 版本
│   │   ├── core/           # 核心配置和工具
│   │   │   ├── config.py  # 应用配置
│   │   │   ├── database.py # 数据库配置
│   │   │   ├── exceptions.py # 异常定义
│   │   │   └── dependencies.py # 依赖注入
│   │   ├── models/        # 数据模型
│   │   ├── repositories/  # 数据访问层
│   │   ├── schemas/       # Pydantic 模式
│   │   ├── services/      # 业务逻辑层
│   │   └── main.py        # 应用入口
│   ├── requirements.txt   # Python 依赖
│   └── .env.example      # 环境变量示例
├── frontend/              # Vue3 前端
│   ├── src/
│   │   ├── api/          # API 接口封装
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # Pinia 状态管理
│   │   ├── types/        # TypeScript 类型定义
│   │   ├── utils/        # 工具函数
│   │   ├── views/        # 页面组件
│   │   └── App.vue       # 根组件
│   ├── package.json      # 前端依赖
│   └── .env.example     # 环境变量示例
└── readme.md
```

## 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端启动

1. 进入后端目录：
```bash
cd backend
```

2. 创建虚拟环境（推荐）：
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

4. 配置环境变量：
```bash
# 复制环境变量示例文件
cp .env.example .env
# 根据需要修改 .env 文件
```

5. 启动服务：
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

后端服务将在 `http://localhost:8000` 启动

### 前端启动

1. 进入前端目录：
```bash
cd frontend
```

2. 安装依赖：
```bash
npm install
# 或
yarn install
```

3. 配置环境变量：
```bash
# 复制环境变量示例文件
cp .env.example .env
# 根据需要修改 .env 文件
```

4. 启动开发服务器：
```bash
npm run dev
# 或
yarn dev
```

前端应用将在 `http://localhost:5173` 启动

## API 文档

启动后端服务后，访问以下地址查看自动生成的 API 文档：

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 架构说明

### 后端架构（FastAPI 最佳实践）

采用分层架构设计：

1. **API 层** (`app/api/`): 处理 HTTP 请求和响应
2. **服务层** (`app/services/`): 业务逻辑处理
3. **仓库层** (`app/repositories/`): 数据访问抽象
4. **模型层** (`app/models/`): 数据库模型定义

设计模式：
- **依赖注入**: 使用 FastAPI 的 Depends
- **仓库模式**: 数据访问层抽象
- **服务层模式**: 业务逻辑封装
- **异常处理**: 统一的异常处理机制

### 前端架构（Vue3 最佳实践）

采用组合式 API 和模块化设计：

1. **类型安全**: 使用 TypeScript 进行类型检查
2. **状态管理**: 使用 Pinia 进行状态管理
3. **API 封装**: 统一的 API 调用接口
4. **组件化**: 可复用的组件设计
5. **路由懒加载**: 优化首屏加载速度

## 使用说明

### 1. 上传文档

- 点击导航栏的"上传文档"
- 拖拽文件或点击上传区域选择文件
- 为每个文档添加描述和标签（可选）
- 点击"上传"按钮

### 2. 管理标签

- 点击导航栏的"标签管理"
- 点击"添加标签"创建新标签
- 可以编辑标签名称和颜色
- 可以删除不需要的标签

### 3. 搜索文档

- 在文档列表页面
- 使用搜索框输入关键词
- 选择标签进行筛选
- 点击"搜索"按钮

### 4. 生成 PDF 汇编

- 在文档列表页面选择多个文档（通过复选框）
- 点击"生成汇编 PDF"按钮
- 系统会自动下载合并后的 PDF 文件

## 数据库

项目使用 SQLite 数据库，数据库文件会自动创建在 `backend/documents.db`

首次运行时会自动创建数据表：
- `documents` - 文档表
- `tags` - 标签表
- `document_tags` - 文档标签关联表

## 文件存储

- 上传的文件存储在 `backend/uploads/` 目录
- 生成的 PDF 文件存储在 `backend/generated_pdfs/` 目录

## 开发说明

### 后端开发

- API 路由定义在 `backend/app/api/v1/` 目录
- 数据模型定义在 `backend/app/models/`
- 业务逻辑在 `backend/app/services/`
- 数据访问在 `backend/app/repositories/`

### 前端开发

- 页面组件在 `frontend/src/views/` 目录
- API 调用封装在 `frontend/src/api/` 目录
- 路由配置在 `frontend/src/router/index.ts`
- 状态管理在 `frontend/src/stores/` 目录

## 注意事项

1. 确保后端服务先启动，前端才能正常调用 API
2. PDF 汇编功能仅支持 PDF 格式文件
3. 上传的文件大小建议不超过 100MB（可在配置中修改）
4. 生产环境建议使用 PostgreSQL 替代 SQLite

## 许可证

MIT License