# 测试说明

## 测试文件结构

```
tests/
├── __init__.py                    # 测试包初始化
├── conftest.py                    # pytest配置和fixtures
├── test_documents_upload.py       # 文档上传接口的pytest测试
├── test_upload_quick.py           # 快速测试脚本（需要服务器运行）
├── README.md                      # 本文件
├── test_upload_analysis.md        # 接口分析与测试指南
└── UPLOAD_INTERFACE_TEST_GUIDE.md # 上传接口测试完整指南
```

## 测试类型

### 1. pytest自动化测试
- **文件**: `test_documents_upload.py`
- **特点**: 使用pytest框架，自动设置测试环境，使用内存数据库
- **运行**: `pytest tests/test_documents_upload.py`

### 2. 快速测试脚本
- **文件**: `test_upload_quick.py`
- **特点**: 需要后端服务运行，使用requests库直接测试API
- **运行**: `python tests/test_upload_quick.py` 或 `python -m tests.test_upload_quick`
- **用途**: 快速验证接口功能，适合手动测试和调试

### 3. 测试文档
- **test_upload_analysis.md**: 详细的接口分析和测试方案
- **UPLOAD_INTERFACE_TEST_GUIDE.md**: 完整的测试指南，包含手动测试方法

## 安装测试依赖

```bash
pip install pytest pytest-asyncio httpx
```

或者添加到 `requirements.txt`：

```txt
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

## 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest tests/test_documents_upload.py
```

### 运行特定测试用例
```bash
pytest tests/test_documents_upload.py::TestDocumentUpload::test_upload_file_only
```

### 显示详细输出
```bash
pytest -v
```

### 显示打印输出
```bash
pytest -s
```

## 测试覆盖

当前测试覆盖 `/api/v1/documents/upload` 接口的以下场景：

1. ✅ 仅上传文件
2. ✅ 上传文件 + 描述
3. ✅ 上传文件 + 标签
4. ✅ 上传文件 + 多个标签
5. ✅ 上传文件 + 描述 + 标签
6. ✅ 不同文件类型（文本文件）
7. ✅ 未指定 content-type 的文件
8. ✅ 缺少文件参数（错误处理）
9. ✅ 无效标签ID处理
10. ✅ 空标签ID字符串
11. ✅ 标签ID包含空格
12. ✅ 文件大小计算
13. ✅ 特殊字符文件名
14. ✅ 连续上传多个文件
15. ✅ 文件名时间戳格式

## 测试配置

- 使用内存数据库（SQLite in-memory）进行测试
- 使用临时目录存储上传的文件
- 测试结束后自动清理

## 快速测试脚本使用

`test_upload_quick.py` 是一个独立的测试脚本，用于快速验证上传接口功能：

```bash
# 确保后端服务已启动
uvicorn app.main:app --reload

# 在另一个终端运行测试脚本
python tests/test_upload_quick.py
```

该脚本会测试以下场景：
- 仅上传文件
- 上传文件 + 描述
- 上传文件 + 标签
- 完整测试（文件 + 描述 + 标签）
- 错误处理（缺少文件）

## 注意事项

1. 测试使用独立的测试数据库，不会影响开发数据库
2. 上传的文件存储在临时目录，测试结束后自动删除
3. 某些测试需要先创建标签，fixture 会自动处理
4. `test_upload_quick.py` 需要后端服务运行，而pytest测试会自动启动测试服务器
