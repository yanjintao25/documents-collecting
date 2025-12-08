# 文档管理系统 - 前端

基于 Vue3 + TypeScript + Element Plus 的文档管理系统前端。

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口封装
│   ├── assets/           # 静态资源
│   ├── components/       # 公共组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia 状态管理
│   ├── types/            # TypeScript 类型定义
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── .env.example          # 环境变量示例
├── package.json          # 依赖配置
└── vite.config.ts        # Vite 配置
```

## 快速开始

### 1. 安装依赖

```bash
npm install
# 或
yarn install
```

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并修改配置：

```bash
cp .env.example .env
```

### 3. 启动开发服务器

```bash
npm run dev
# 或
yarn dev
```

应用将在 http://localhost:5173 启动

### 4. 构建生产版本

```bash
npm run build
# 或
yarn build
```

## 技术栈

- **Vue 3**: 渐进式 JavaScript 框架
- **TypeScript**: 类型安全的 JavaScript 超集
- **Vite**: 下一代前端构建工具
- **Vue Router**: 官方路由管理器
- **Pinia**: 状态管理库
- **Element Plus**: Vue 3 组件库
- **Axios**: HTTP 客户端

## 代码规范

- 使用组合式 API (Composition API)
- 使用 TypeScript 进行类型检查
- 遵循 Vue 3 最佳实践
- 组件和函数使用清晰的命名

