# `/documents/upload` 接口分析与测试指南

## 一、接口分析

### 1.1 接口基本信息

- **路径**: `POST /api/v1/documents/upload`
- **功能**: 上传文档文件到服务器
- **状态码**: 201 (Created)
- **响应格式**: JSON (DocumentResponse)

### 1.2 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `file` | UploadFile | ✅ | 上传的文件（multipart/form-data） |
| `description` | string | ❌ | 文档描述（Form字段） |
| `tag_ids` | string | ❌ | 标签ID，逗号分隔（如 "1,2,3"） |

### 1.3 响应结构

```json
{
  "id": 1,
  "filename": "20241201_120000_example.pdf",
  "original_filename": "example.pdf",
  "file_path": "uploads/20241201_120000_example.pdf",
  "file_size": 1024,
  "file_type": "application/pdf",
  "description": "这是一个示例文档",
  "upload_time": "2024-12-01T12:00:00",
  "tags": [
    {
      "id": 1,
      "name": "重要",
      "color": "#409EFF",
      "created_at": "2024-12-01T10:00:00"
    }
  ]
}
```

### 1.4 处理流程

```
1. API层接收 multipart/form-data 请求
   ↓
2. 解析 tag_ids 字符串为整数列表（如 "1,2,3" → [1,2,3]）
   ↓
3. 调用 DocumentService.upload_document()
   ↓
4. Service层：
   - 生成唯一文件名（时间戳_原文件名）
   - 保存文件到 uploads/ 目录
   - 获取文件大小
   - 调用 Repository 创建数据库记录
   ↓
5. Repository层：
   - 创建 Document 模型实例
   - 关联标签（如果提供 tag_ids）
   - 保存到数据库
   ↓
6. 返回 DocumentResponse
```

### 1.5 关键逻辑

1. **文件名生成**: `{timestamp}_{original_filename}`
   - 时间戳格式: `YYYYMMDD_HHMMSS`
   - 避免文件名冲突

2. **标签关联**: 
   - 如果提供 `tag_ids`，会查询数据库验证标签是否存在
   - 建立文档与标签的多对多关系

3. **文件存储**:
   - 存储路径: `backend/uploads/`
   - 文件类型从 `UploadFile.content_type` 获取
   - 如果 content_type 为空，默认为 `application/octet-stream`

---

## 二、测试方案

### 2.1 测试场景

#### ✅ 正常场景
1. **仅上传文件**（无描述、无标签）
2. **上传文件 + 描述**
3. **上传文件 + 标签**
4. **上传文件 + 描述 + 标签**
5. **不同文件类型**（PDF、DOC、TXT、图片等）

#### ❌ 异常场景
1. **缺少文件**（file 参数缺失）
2. **无效标签ID**（标签不存在）
3. **文件过大**（超过限制，虽然代码中未实现）
4. **空文件**
5. **特殊字符文件名**

---

## 三、手动测试方法

### 3.1 使用 Swagger UI（推荐）

1. 启动后端服务：
   ```bash
   uvicorn app.main:app --reload
   ```

2. 访问 Swagger UI：
   ```
   http://localhost:8000/docs
   ```

3. 找到 `POST /api/v1/documents/upload` 接口

4. 点击 "Try it out"

5. 填写参数：
   - `file`: 点击 "Choose File" 选择文件
   - `description`: 输入描述（可选）
   - `tag_ids`: 输入标签ID，如 "1,2"（可选）

6. 点击 "Execute"

7. 查看响应结果

### 3.2 使用 Postman

1. **创建请求**:
   - Method: `POST`
   - URL: `http://localhost:8000/api/v1/documents/upload`

2. **设置 Body**:
   - 选择 `form-data`
   - 添加字段：
     - `file`: 类型选择 `File`，选择文件
     - `description`: 类型选择 `Text`，输入描述（可选）
     - `tag_ids`: 类型选择 `Text`，输入 "1,2"（可选）

3. **发送请求**

4. **查看响应**

### 3.3 使用 cURL

```bash
# 基本上传（仅文件）
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf"

# 上传文件 + 描述
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf" \
  -F "description=这是一个测试文档"

# 上传文件 + 描述 + 标签
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/path/to/your/file.pdf" \
  -F "description=这是一个测试文档" \
  -F "tag_ids=1,2,3"
```

### 3.4 使用 Python requests

```python
import requests

url = "http://localhost:8000/api/v1/documents/upload"

# 测试1: 仅上传文件
with open("test.pdf", "rb") as f:
    files = {"file": ("test.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)
    print(response.json())

# 测试2: 上传文件 + 描述 + 标签
with open("test.pdf", "rb") as f:
    files = {"file": ("test.pdf", f, "application/pdf")}
    data = {
        "description": "这是一个测试文档",
        "tag_ids": "1,2"
    }
    response = requests.post(url, files=files, data=data)
    print(response.json())
```

---

## 四、自动化测试

### 4.1 测试依赖

在 `requirements.txt` 中添加测试依赖：

```txt
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.2
```

安装：
```bash
pip install pytest pytest-asyncio httpx
```

### 4.2 测试文件结构

```
backend/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # 测试配置和fixtures
│   └── test_documents.py    # 文档接口测试
```

### 4.3 测试代码示例

详见 `tests/test_documents_upload.py`

---

## 五、验证要点

### 5.1 响应验证

- ✅ 状态码为 201
- ✅ 返回的 JSON 包含所有必需字段
- ✅ `id` 字段存在且为整数
- ✅ `filename` 包含时间戳前缀
- ✅ `original_filename` 与上传文件名一致
- ✅ `file_path` 指向正确的存储路径
- ✅ `file_size` 与实际文件大小一致
- ✅ `file_type` 正确识别
- ✅ `upload_time` 为有效时间戳

### 5.2 文件系统验证

- ✅ 文件已保存到 `uploads/` 目录
- ✅ 文件名格式正确（时间戳_原文件名）
- ✅ 文件内容完整（可以下载验证）

### 5.3 数据库验证

- ✅ 数据库中存在新记录
- ✅ 所有字段正确保存
- ✅ 标签关联正确（如果提供）

### 5.4 边界情况验证

- ✅ 空文件处理
- ✅ 大文件处理（如果有限制）
- ✅ 特殊字符文件名
- ✅ 无效标签ID处理

---

## 六、常见问题

### Q1: 上传失败，返回 422 错误
**原因**: 请求格式不正确
**解决**: 确保使用 `multipart/form-data` 格式，`file` 字段必须存在

### Q2: 标签关联失败
**原因**: 提供的标签ID不存在
**解决**: 先创建标签，或使用已存在的标签ID

### Q3: 文件未保存
**原因**: `uploads/` 目录权限问题或路径错误
**解决**: 检查目录权限，确保应用有写入权限

### Q4: 文件名乱码
**原因**: 文件名包含特殊字符或非ASCII字符
**解决**: 代码中可能需要处理文件名编码

---

## 七、性能测试建议

1. **小文件** (< 1MB): 测试响应时间
2. **中等文件** (1-10MB): 测试上传速度
3. **大文件** (> 10MB): 测试超时和内存使用
4. **并发上传**: 测试多用户同时上传

---

## 八、安全测试建议

1. **文件类型验证**: 测试上传恶意文件（.exe, .sh等）
2. **文件大小限制**: 测试超大文件上传
3. **路径遍历攻击**: 测试文件名包含 `../` 的情况
4. **SQL注入**: 测试描述字段中的SQL注入尝试

