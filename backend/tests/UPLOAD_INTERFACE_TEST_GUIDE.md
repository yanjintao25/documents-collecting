# `/documents/upload` 接口测试完整指南

## 📋 目录

1. [接口分析](#接口分析)
2. [快速开始](#快速开始)
3. [手动测试方法](#手动测试方法)
4. [自动化测试](#自动化测试)
5. [测试场景清单](#测试场景清单)

---

## 🔍 接口分析

### 接口信息

- **端点**: `POST /api/v1/documents/upload`
- **Content-Type**: `multipart/form-data`
- **响应状态码**: `201 Created`
- **响应格式**: JSON

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | File | ✅ | 上传的文件 |
| `description` | String | ❌ | 文档描述 |
| `tag_ids` | String | ❌ | 标签ID，逗号分隔（如 "1,2,3"） |

### 响应示例

```json
{
  "id": 1,
  "filename": "20241201_120000_example.pdf",
  "original_filename": "example.pdf",
  "file_path": "uploads/20241201_120000_example.pdf",
  "file_size": 1024,
  "file_type": "application/pdf",
  "description": "文档描述",
  "upload_time": "2024-12-01T12:00:00",
  "tags": []
}
```

### 处理流程

```
客户端请求
  ↓
API层 (documents.py)
  ↓ 解析 tag_ids 字符串
Service层 (document_service.py)
  ↓ 生成文件名、保存文件
Repository层 (document_repository.py)
  ↓ 创建数据库记录、关联标签
数据库
  ↓
返回 DocumentResponse
```

---

## 🚀 快速开始

### 1. 启动后端服务

```bash
cd backend
uvicorn app.main:app --reload
```

### 2. 运行快速测试脚本

```bash
# 从backend目录运行
python tests/test_upload_quick.py

# 或者使用模块方式
python -m tests.test_upload_quick
```

这个脚本会自动测试多个场景，包括：
- ✅ 仅上传文件
- ✅ 上传文件 + 描述
- ✅ 上传文件 + 标签
- ✅ 完整测试（文件 + 描述 + 标签）
- ✅ 错误处理（缺少文件）

---

## 🧪 手动测试方法

### 方法1: Swagger UI（推荐 ⭐）

1. 访问 `http://localhost:8000/docs`
2. 找到 `POST /api/v1/documents/upload`
3. 点击 "Try it out"
4. 选择文件，填写可选参数
5. 点击 "Execute"
6. 查看响应结果

**优点**: 
- 可视化界面
- 自动生成请求格式
- 可以直接查看响应

### 方法2: Postman

1. 创建新请求
   - Method: `POST`
   - URL: `http://localhost:8000/api/v1/documents/upload`

2. Body 设置
   - 选择 `form-data`
   - 添加字段：
     - `file`: 类型 `File`，选择文件
     - `description`: 类型 `Text`（可选）
     - `tag_ids`: 类型 `Text`（可选）

3. 发送请求

### 方法3: cURL

```bash
# 基本上传
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/path/to/file.pdf"

# 完整参数
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/path/to/file.pdf" \
  -F "description=文档描述" \
  -F "tag_ids=1,2,3"
```

### 方法4: Python requests

```python
import requests

url = "http://localhost:8000/api/v1/documents/upload"

with open("test.pdf", "rb") as f:
    files = {"file": ("test.pdf", f, "application/pdf")}
    data = {
        "description": "测试文档",
        "tag_ids": "1,2"
    }
    response = requests.post(url, files=files, data=data)
    print(response.json())
```

---

## 🤖 自动化测试

### 安装测试依赖

```bash
pip install pytest pytest-asyncio httpx
```

### 运行测试

```bash
# 运行所有测试
pytest tests/

# 运行特定测试文件
pytest tests/test_documents_upload.py

# 显示详细输出
pytest -v

# 显示打印输出
pytest -s
```

### 测试覆盖

测试文件 `tests/test_documents_upload.py` 包含 15 个测试用例，覆盖：

1. ✅ 仅上传文件
2. ✅ 上传文件 + 描述
3. ✅ 上传文件 + 单个标签
4. ✅ 上传文件 + 多个标签
5. ✅ 上传文件 + 描述 + 标签
6. ✅ 不同文件类型（文本文件）
7. ✅ 未指定 content-type
8. ✅ 缺少文件参数（错误处理）
9. ✅ 无效标签ID处理
10. ✅ 空标签ID字符串
11. ✅ 标签ID包含空格
12. ✅ 文件大小计算
13. ✅ 特殊字符文件名
14. ✅ 连续上传多个文件
15. ✅ 文件名时间戳格式验证

---

## ✅ 测试场景清单

### 正常场景

- [x] **场景1**: 仅上传文件（无描述、无标签）
  - 验证: 文件保存、数据库记录创建、返回正确响应

- [x] **场景2**: 上传文件 + 描述
  - 验证: 描述正确保存

- [x] **场景3**: 上传文件 + 标签
  - 验证: 标签正确关联

- [x] **场景4**: 上传文件 + 多个标签
  - 验证: 所有标签正确关联

- [x] **场景5**: 上传文件 + 描述 + 标签
  - 验证: 所有字段正确保存

- [x] **场景6**: 不同文件类型
  - 测试: PDF、TXT、DOC、图片等
  - 验证: 文件类型正确识别

### 异常场景

- [x] **场景7**: 缺少文件参数
  - 预期: 返回 422 错误

- [x] **场景8**: 无效标签ID
  - 验证: 不报错，但不关联标签

- [x] **场景9**: 空文件
  - 验证: 可以上传，文件大小为 0

- [x] **场景10**: 特殊字符文件名
  - 测试: 中文、空格、特殊符号
  - 验证: 文件名正确处理

### 边界测试

- [x] **场景11**: 大文件上传
  - 注意: 当前代码未实现大小限制

- [x] **场景12**: 并发上传
  - 测试: 同时上传多个文件

- [x] **场景13**: 文件名长度
  - 测试: 超长文件名

---

## 📝 验证要点

### 响应验证

- ✅ 状态码为 201
- ✅ 返回 JSON 包含所有必需字段
- ✅ `id` 字段存在且为整数
- ✅ `filename` 包含时间戳前缀
- ✅ `original_filename` 与上传文件名一致
- ✅ `file_path` 指向正确的存储路径
- ✅ `file_size` 与实际文件大小一致
- ✅ `file_type` 正确识别
- ✅ `upload_time` 为有效时间戳

### 文件系统验证

- ✅ 文件已保存到 `uploads/` 目录
- ✅ 文件名格式正确（时间戳_原文件名）
- ✅ 文件内容完整（可以下载验证）

### 数据库验证

- ✅ 数据库中存在新记录
- ✅ 所有字段正确保存
- ✅ 标签关联正确（如果提供）

---

## 🐛 常见问题

### Q1: 返回 422 错误

**原因**: 请求格式不正确

**解决**: 
- 确保使用 `multipart/form-data` 格式
- 确保 `file` 字段存在
- 检查 Content-Type 头

### Q2: 标签关联失败

**原因**: 提供的标签ID不存在

**解决**: 
- 先创建标签（`POST /api/v1/tags/`）
- 使用已存在的标签ID
- 检查标签ID格式（逗号分隔）

### Q3: 文件未保存

**原因**: 目录权限问题

**解决**: 
- 检查 `uploads/` 目录权限
- 确保应用有写入权限
- 检查磁盘空间

### Q4: 文件名乱码

**原因**: 文件名包含特殊字符

**解决**: 
- 代码会自动处理
- 如果仍有问题，检查文件编码

---

## 📚 相关文件

- **接口定义**: `app/api/v1/documents.py`
- **业务逻辑**: `app/services/document_service.py`
- **数据访问**: `app/repositories/document_repository.py`
- **数据模型**: `app/models/document.py`
- **响应模式**: `app/schemas/document.py`
- **测试文件**: `tests/test_documents_upload.py`
- **快速测试**: `tests/test_upload_quick.py`
- **详细分析**: `tests/test_upload_analysis.md`

---

## 🎯 下一步

1. **性能测试**: 测试大文件上传和并发性能
2. **安全测试**: 测试文件类型验证、路径遍历攻击等
3. **集成测试**: 测试与其他接口的集成
4. **压力测试**: 测试系统在高负载下的表现

---

## 📞 支持

如有问题，请查看：
- API 文档: `http://localhost:8000/docs`
- 项目 README: `README.md`
- 测试分析: `tests/test_upload_analysis.md`

