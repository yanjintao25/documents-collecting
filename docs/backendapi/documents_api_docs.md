# Documents API 接口调用文档

本文档详细说明了 `documents.py` 中各个接口的调用方法和用例。

**基础URL**: `/api/v1/documents`

---

## 1. 上传文档

### 接口信息
- **方法**: `POST`
- **路径**: `/api/v1/documents/upload`
- **状态码**: `201 Created`
- **描述**: 上传一个新文档文件

### 请求参数
**请求类型**: `multipart/form-data`

**表单字段**:
- `file` (File, 必填): 要上传的文件
- `description` (String, 可选): 文档描述
- `category_id` (Integer, 可选): 分类ID

### 响应格式
```json
{
  "id": 1,
  "title": "example.pdf",
  "file_size": 1024000,
  "file_type": "application/pdf",
  "pdf_file_size": 1024000,
  "introduction": null,
  "write_time": null,
  "status": 1,
  "upload_user_name": "admin",
  "upload_user_id": "1",
  "update_user_name": null,
  "update_user_id": null,
  "category_id": 1,
  "category_name": "技术文档",
  "create_time": "2024-01-01T12:00:00",
  "update_time": "2024-01-01T12:00:00",
  "description": null,
  "tags": []
}
```

### 调用示例

#### cURL
```bash
# 基本上传
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/path/to/document.pdf"

# 带描述和分类的上传
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -F "file=@/path/to/document.pdf" \
  -F "description=这是一份技术文档" \
  -F "category_id=1"
```

#### Python (requests)
```python
import requests

url = "http://localhost:8000/api/v1/documents/upload"

# 基本上传
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    response = requests.post(url, files=files)
    print(response.status_code)  # 201
    print(response.json())

# 带描述和分类的上传
with open("document.pdf", "rb") as f:
    files = {"file": ("document.pdf", f, "application/pdf")}
    data = {
        "description": "这是一份技术文档",
        "category_id": 1
    }
    response = requests.post(url, files=files, data=data)
    print(response.status_code)  # 201
    print(response.json())
```

#### JavaScript (fetch)
```javascript
// 基本上传
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/api/v1/documents/upload', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// 带描述和分类的上传
const formData = new FormData();
formData.append('file', fileInput.files[0]);
formData.append('description', '这是一份技术文档');
formData.append('category_id', '1');

fetch('http://localhost:8000/api/v1/documents/upload', {
  method: 'POST',
  body: formData
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    with open("document.pdf", "rb") as f:
        files = {"file": ("document.pdf", f, "application/pdf")}
        data = {
            "description": "这是一份技术文档",
            "category_id": 1
        }
        response = await client.post(
            "http://localhost:8000/api/v1/documents/upload",
            files=files,
            data=data
        )
        print(response.status_code)  # 201
        print(response.json())
```

### 错误情况
- **400 Bad Request**: 文件格式不支持或文件损坏
- **422 Unprocessable Entity**: 请求参数验证失败

---

## 2. 获取文档列表

### 接口信息
- **方法**: `GET`
- **路径**: `/api/v1/documents/`
- **状态码**: `200 OK`
- **描述**: 获取文档列表，支持分页

### 请求参数
**查询参数**:
- `skip` (Integer, 可选): 跳过的记录数，默认值为 `0`
- `limit` (Integer, 可选): 返回的记录数限制，默认值为 `100`

### 响应格式
```json
[
  {
    "id": 1,
    "title": "example.pdf",
    "file_size": 1024000,
    "file_type": "application/pdf",
    "pdf_file_size": 1024000,
    "introduction": null,
    "write_time": null,
    "status": 1,
    "upload_user_name": "admin",
    "upload_user_id": "1",
    "update_user_name": null,
    "update_user_id": null,
    "category_id": 1,
    "category_name": "技术文档",
    "create_time": "2024-01-01T12:00:00",
    "update_time": "2024-01-01T12:00:00",
    "description": null,
    "tags": [
      {
        "id": 1,
        "name": "重要"
      }
    ]
  }
]
```

### 调用示例

#### cURL
```bash
# 获取所有文档（默认前100条）
curl -X GET "http://localhost:8000/api/v1/documents/"

# 分页获取：跳过前10条，获取20条
curl -X GET "http://localhost:8000/api/v1/documents/?skip=10&limit=20"
```

#### Python (requests)
```python
import requests

url = "http://localhost:8000/api/v1/documents/"

# 获取所有文档
response = requests.get(url)
print(response.status_code)  # 200
print(response.json())

# 分页获取
params = {"skip": 10, "limit": 20}
response = requests.get(url, params=params)
print(response.status_code)  # 200
print(response.json())
```

#### JavaScript (fetch)
```javascript
// 获取所有文档
fetch('http://localhost:8000/api/v1/documents/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// 分页获取
const params = new URLSearchParams({
  skip: '10',
  limit: '20'
});
fetch(`http://localhost:8000/api/v1/documents/?${params}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    # 获取所有文档
    response = await client.get("http://localhost:8000/api/v1/documents/")
    print(response.status_code)  # 200
    print(response.json())
    
    # 分页获取
    params = {"skip": 10, "limit": 20}
    response = await client.get(
        "http://localhost:8000/api/v1/documents/",
        params=params
    )
    print(response.status_code)  # 200
    print(response.json())
```

---

## 3. 获取单个文档信息

### 接口信息
- **方法**: `GET`
- **路径**: `/api/v1/documents/{document_id}`
- **状态码**: `200 OK`
- **描述**: 根据ID获取单个文档的详细信息

### 请求参数
**路径参数**:
- `document_id` (int): 文档ID，必填

### 响应格式
```json
{
  "id": 1,
  "title": "example.pdf",
  "file_size": 1024000,
  "file_type": "application/pdf",
  "pdf_file_size": 1024000,
  "introduction": "文档简介",
  "write_time": "2024-01-01T10:00:00",
  "status": 1,
  "upload_user_name": "admin",
  "upload_user_id": "1",
  "update_user_name": "admin",
  "update_user_id": "1",
  "category_id": 1,
  "category_name": "技术文档",
  "create_time": "2024-01-01T12:00:00",
  "update_time": "2024-01-01T14:00:00",
  "description": "文档简介",
  "tags": [
    {
      "id": 1,
      "name": "重要"
    },
    {
      "id": 2,
      "name": "技术"
    }
  ]
}
```

### 调用示例

#### cURL
```bash
curl -X GET "http://localhost:8000/api/v1/documents/1"
```

#### Python (requests)
```python
import requests

document_id = 1
url = f"http://localhost:8000/api/v1/documents/{document_id}"
response = requests.get(url)
print(response.status_code)  # 200
print(response.json())
```

#### JavaScript (fetch)
```javascript
const documentId = 1;
fetch(`http://localhost:8000/api/v1/documents/${documentId}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    document_id = 1
    response = await client.get(f"http://localhost:8000/api/v1/documents/{document_id}")
    print(response.status_code)  # 200
    print(response.json())
```

### 错误情况
- **404 Not Found**: 文档不存在

---

## 4. 下载文档

### 接口信息
- **方法**: `GET`
- **路径**: `/api/v1/documents/{document_id}/download`
- **状态码**: `200 OK`
- **描述**: 下载指定的文档文件
- **Content-Type**: 根据文件类型自动设置（如 `application/pdf`）

### 请求参数
**路径参数**:
- `document_id` (int): 文档ID，必填

### 响应格式
文件流（二进制数据）

### 调用示例

#### cURL
```bash
# 下载文档并保存到本地
curl -X GET "http://localhost:8000/api/v1/documents/1/download" \
  -o "downloaded_document.pdf"

# 查看响应头信息
curl -X GET "http://localhost:8000/api/v1/documents/1/download" \
  -I
```

#### Python (requests)
```python
import requests

document_id = 1
url = f"http://localhost:8000/api/v1/documents/{document_id}/download"
response = requests.get(url, stream=True)

if response.status_code == 200:
    # 获取文件名（从响应头）
    content_disposition = response.headers.get('content-disposition', '')
    filename = content_disposition.split('filename=')[1].strip('"') if 'filename=' in content_disposition else f"document_{document_id}"
    
    # 保存文件
    with open(filename, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"文件已保存: {filename}")
else:
    print(f"下载失败: {response.status_code}")
```

#### JavaScript (fetch)
```javascript
const documentId = 1;
fetch(`http://localhost:8000/api/v1/documents/${documentId}/download`)
  .then(response => {
    if (!response.ok) {
      throw new Error('下载失败');
    }
    return response.blob();
  })
  .then(blob => {
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `document_${documentId}`;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  })
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    document_id = 1
    async with client.stream(
        "GET",
        f"http://localhost:8000/api/v1/documents/{document_id}/download"
    ) as response:
        if response.status_code == 200:
            filename = f"document_{document_id}.pdf"
            with open(filename, 'wb') as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
            print(f"文件已保存: {filename}")
        else:
            print(f"下载失败: {response.status_code}")
```

### 错误情况
- **404 Not Found**: 文档不存在或文件不存在

---

## 5. 更新文档信息

### 接口信息
- **方法**: `PUT`
- **路径**: `/api/v1/documents/{document_id}`
- **状态码**: `200 OK`
- **描述**: 更新文档的信息（描述、标签等）

### 请求参数
**路径参数**:
- `document_id` (int): 文档ID，必填

**请求体 (JSON)**:
```json
{
  "description": "更新后的文档描述",  // 可选
  "tag_ids": [1, 2, 3]  // 可选，标签ID列表
}
```

### 响应格式
```json
{
  "id": 1,
  "title": "example.pdf",
  "file_size": 1024000,
  "file_type": "application/pdf",
  "pdf_file_size": 1024000,
  "introduction": "更新后的文档描述",
  "write_time": null,
  "status": 1,
  "upload_user_name": "admin",
  "upload_user_id": "1",
  "update_user_name": "admin",
  "update_user_id": "1",
  "category_id": 1,
  "category_name": "技术文档",
  "create_time": "2024-01-01T12:00:00",
  "update_time": "2024-01-01T15:00:00",
  "description": "更新后的文档描述",
  "tags": [
    {
      "id": 1,
      "name": "重要"
    },
    {
      "id": 2,
      "name": "技术"
    },
    {
      "id": 3,
      "name": "文档"
    }
  ]
}
```

### 调用示例

#### cURL
```bash
# 只更新描述
curl -X PUT "http://localhost:8000/api/v1/documents/1" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "更新后的文档描述"
  }'

# 只更新标签
curl -X PUT "http://localhost:8000/api/v1/documents/1" \
  -H "Content-Type: application/json" \
  -d '{
    "tag_ids": [1, 2, 3]
  }'

# 同时更新描述和标签
curl -X PUT "http://localhost:8000/api/v1/documents/1" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "更新后的文档描述",
    "tag_ids": [1, 2, 3]
  }'
```

#### Python (requests)
```python
import requests

document_id = 1
url = f"http://localhost:8000/api/v1/documents/{document_id}"

# 只更新描述
data = {"description": "更新后的文档描述"}
response = requests.put(url, json=data)
print(response.status_code)  # 200
print(response.json())

# 只更新标签
data = {"tag_ids": [1, 2, 3]}
response = requests.put(url, json=data)
print(response.status_code)  # 200
print(response.json())

# 同时更新描述和标签
data = {
    "description": "更新后的文档描述",
    "tag_ids": [1, 2, 3]
}
response = requests.put(url, json=data)
print(response.status_code)  # 200
print(response.json())
```

#### JavaScript (fetch)
```javascript
const documentId = 1;

// 只更新描述
fetch(`http://localhost:8000/api/v1/documents/${documentId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    description: '更新后的文档描述'
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

// 同时更新描述和标签
fetch(`http://localhost:8000/api/v1/documents/${documentId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    description: '更新后的文档描述',
    tag_ids: [1, 2, 3]
  })
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    document_id = 1
    data = {
        "description": "更新后的文档描述",
        "tag_ids": [1, 2, 3]
    }
    response = await client.put(
        f"http://localhost:8000/api/v1/documents/{document_id}",
        json=data
    )
    print(response.status_code)  # 200
    print(response.json())
```

### 错误情况
- **400 Bad Request**: 请求参数验证失败
- **404 Not Found**: 文档不存在

---

## 6. 删除文档

### 接口信息
- **方法**: `DELETE`
- **路径**: `/api/v1/documents/{document_id}`
- **状态码**: `204 No Content`
- **描述**: 删除指定的文档

### 请求参数
**路径参数**:
- `document_id` (int): 文档ID，必填

### 响应格式
无响应体（204状态码）

### 调用示例

#### cURL
```bash
curl -X DELETE "http://localhost:8000/api/v1/documents/1"
```

#### Python (requests)
```python
import requests

document_id = 1
url = f"http://localhost:8000/api/v1/documents/{document_id}"
response = requests.delete(url)
print(response.status_code)  # 204
# 无响应体
```

#### JavaScript (fetch)
```javascript
const documentId = 1;
fetch(`http://localhost:8000/api/v1/documents/${documentId}`, {
  method: 'DELETE'
})
  .then(response => {
    if (response.status === 204) {
      console.log('文档删除成功');
    }
  })
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    document_id = 1
    response = await client.delete(f"http://localhost:8000/api/v1/documents/{document_id}")
    print(response.status_code)  # 204
```

### 错误情况
- **404 Not Found**: 文档不存在

---

## 完整用例示例

### 用例1: 完整的CRUD操作流程

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/documents"

# 1. 上传文档
print("=== 上传文档 ===")
with open("test_document.pdf", "rb") as f:
    files = {"file": ("test_document.pdf", f, "application/pdf")}
    data = {
        "description": "测试文档",
        "category_id": 1
    }
    upload_response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
    document = upload_response.json()
    print(f"上传成功: {document}")
    document_id = document["id"]

# 2. 获取文档列表
print("\n=== 获取文档列表 ===")
documents = requests.get(f"{BASE_URL}/").json()
print(f"文档列表: {len(documents)} 个文档")

# 3. 获取单个文档
print("\n=== 获取单个文档 ===")
single_document = requests.get(f"{BASE_URL}/{document_id}").json()
print(f"文档详情: {single_document['title']}")

# 4. 更新文档
print("\n=== 更新文档 ===")
update_data = {
    "description": "更新后的描述",
    "tag_ids": [1, 2]
}
updated_document = requests.put(f"{BASE_URL}/{document_id}", json=update_data).json()
print(f"更新成功: {updated_document['description']}")

# 5. 下载文档
print("\n=== 下载文档 ===")
download_response = requests.get(f"{BASE_URL}/{document_id}/download", stream=True)
if download_response.status_code == 200:
    with open("downloaded_document.pdf", "wb") as f:
        for chunk in download_response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("下载成功")

# 6. 删除文档
print("\n=== 删除文档 ===")
delete_response = requests.delete(f"{BASE_URL}/{document_id}")
print(f"删除状态码: {delete_response.status_code}")  # 204
```

### 用例2: 批量上传文档

```python
import requests
import os
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1/documents"
documents_dir = Path("./documents")

uploaded_documents = []

# 批量上传目录中的所有PDF文件
for pdf_file in documents_dir.glob("*.pdf"):
    print(f"上传文件: {pdf_file.name}")
    with open(pdf_file, "rb") as f:
        files = {"file": (pdf_file.name, f, "application/pdf")}
        data = {
            "description": f"批量上传的文档: {pdf_file.name}",
            "category_id": 1
        }
        response = requests.post(f"{BASE_URL}/upload", files=files, data=data)
        if response.status_code == 201:
            uploaded_documents.append(response.json())
            print(f"✓ 上传成功: {pdf_file.name}")
        else:
            print(f"✗ 上传失败: {pdf_file.name} - {response.status_code}")

print(f"\n总共上传了 {len(uploaded_documents)} 个文档")
```

### 用例3: 分页获取文档列表

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/documents"

def get_all_documents(page_size=50):
    """分页获取所有文档"""
    all_documents = []
    skip = 0
    
    while True:
        params = {"skip": skip, "limit": page_size}
        response = requests.get(f"{BASE_URL}/", params=params)
        documents = response.json()
        
        if not documents:
            break
        
        all_documents.extend(documents)
        skip += page_size
        
        # 如果返回的文档数少于page_size，说明已经是最后一页
        if len(documents) < page_size:
            break
    
    return all_documents

# 获取所有文档
all_docs = get_all_documents(page_size=50)
print(f"总共获取了 {len(all_docs)} 个文档")
```

### 用例4: 更新文档标签

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/documents"

def update_document_tags(document_id, tag_ids):
    """更新文档的标签"""
    data = {"tag_ids": tag_ids}
    response = requests.put(f"{BASE_URL}/{document_id}", json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"更新失败: {response.status_code}")
        return None

# 为文档添加标签
document_id = 1
tag_ids = [1, 2, 3]  # 标签ID列表
updated_doc = update_document_tags(document_id, tag_ids)
if updated_doc:
    print(f"文档标签已更新: {[tag['name'] for tag in updated_doc['tags']]}")
```

### 用例5: 批量下载文档

```python
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1/documents"
download_dir = Path("./downloads")
download_dir.mkdir(exist_ok=True)

# 获取所有文档
documents = requests.get(f"{BASE_URL}/").json()

# 批量下载
for doc in documents:
    doc_id = doc["id"]
    doc_title = doc["title"]
    print(f"下载文档: {doc_title}")
    
    response = requests.get(f"{BASE_URL}/{doc_id}/download", stream=True)
    if response.status_code == 200:
        file_path = download_dir / doc_title
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✓ 下载成功: {doc_title}")
    else:
        print(f"✗ 下载失败: {doc_title} - {response.status_code}")
```

### 用例6: 错误处理示例

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/documents"

# 上传不存在的文件
try:
    with open("nonexistent.pdf", "rb") as f:
        files = {"file": ("nonexistent.pdf", f, "application/pdf")}
        response = requests.post(f"{BASE_URL}/upload", files=files)
        if response.status_code != 201:
            print(f"上传失败: {response.status_code}")
except FileNotFoundError:
    print("错误: 文件不存在")

# 获取不存在的文档
try:
    response = requests.get(f"{BASE_URL}/99999")
    if response.status_code == 404:
        print("错误: 文档不存在")
except Exception as e:
    print(f"请求错误: {e}")

# 更新不存在的文档
try:
    response = requests.put(
        f"{BASE_URL}/99999",
        json={"description": "测试"}
    )
    if response.status_code == 404:
        print("错误: 文档不存在")
except Exception as e:
    print(f"请求错误: {e}")

# 下载不存在的文档
try:
    response = requests.get(f"{BASE_URL}/99999/download")
    if response.status_code == 404:
        print("错误: 文档不存在或文件不存在")
except Exception as e:
    print(f"请求错误: {e}")
```

---

## 注意事项

1. **基础URL**: 请根据实际部署情况修改 `http://localhost:8000` 为实际的服务器地址

2. **文件上传**:
   - 上传接口使用 `multipart/form-data` 格式
   - 文件字段名必须为 `file`
   - 支持的文件类型取决于服务器配置

3. **文件下载**:
   - 下载接口返回文件流，需要正确处理二进制数据
   - 建议使用流式下载（`stream=True`）处理大文件
   - 文件名可以从响应头的 `Content-Disposition` 中获取

4. **分页参数**:
   - `skip`: 跳过的记录数（从0开始）
   - `limit`: 每页返回的记录数
   - 默认值：`skip=0`, `limit=100`

5. **状态码**:
   - 创建成功返回 `201`
   - 删除成功返回 `204`（无响应体）
   - 其他成功操作返回 `200`

6. **文档更新**:
   - `description` 和 `tag_ids` 都是可选字段
   - 可以只更新其中一个字段
   - `tag_ids` 为空列表 `[]` 表示移除所有标签

7. **错误处理**: 建议在实际使用中检查响应状态码并处理错误情况

---

## FastAPI 自动文档

FastAPI 提供了自动生成的交互式API文档，可以通过以下地址访问：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

在这些文档中，你可以直接测试所有接口，包括文件上传功能。

---

## 前端集成示例

### Vue 3 + TypeScript 示例

```typescript
// api/documents.ts
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1/documents';

export interface Document {
  id: number;
  title: string;
  file_size: number;
  file_type: string;
  description?: string;
  category_id?: number;
  tags: Array<{ id: number; name: string }>;
  // ... 其他字段
}

export interface DocumentUpdate {
  description?: string;
  tag_ids?: number[];
}

// 上传文档
export async function uploadDocument(
  file: File,
  description?: string,
  categoryId?: number
): Promise<Document> {
  const formData = new FormData();
  formData.append('file', file);
  if (description) formData.append('description', description);
  if (categoryId) formData.append('category_id', categoryId.toString());

  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  return response.data;
}

// 获取文档列表
export async function getDocuments(skip = 0, limit = 100): Promise<Document[]> {
  const response = await axios.get(`${API_BASE}/`, {
    params: { skip, limit }
  });
  return response.data;
}

// 获取单个文档
export async function getDocument(id: number): Promise<Document> {
  const response = await axios.get(`${API_BASE}/${id}`);
  return response.data;
}

// 下载文档
export async function downloadDocument(id: number): Promise<Blob> {
  const response = await axios.get(`${API_BASE}/${id}/download`, {
    responseType: 'blob'
  });
  return response.data;
}

// 更新文档
export async function updateDocument(
  id: number,
  data: DocumentUpdate
): Promise<Document> {
  const response = await axios.put(`${API_BASE}/${id}`, data);
  return response.data;
}

// 删除文档
export async function deleteDocument(id: number): Promise<void> {
  await axios.delete(`${API_BASE}/${id}`);
}
```

### React 示例

```typescript
// hooks/useDocuments.ts
import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1/documents';

export function useDocuments() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchDocuments = async (skip = 0, limit = 100) => {
    setLoading(true);
    try {
      const response = await axios.get(`${API_BASE}/`, {
        params: { skip, limit }
      });
      setDocuments(response.data);
    } catch (error) {
      console.error('获取文档列表失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const uploadDocument = async (
    file: File,
    description?: string,
    categoryId?: number
  ) => {
    const formData = new FormData();
    formData.append('file', file);
    if (description) formData.append('description', description);
    if (categoryId) formData.append('category_id', categoryId.toString());

    try {
      const response = await axios.post(`${API_BASE}/upload`, formData);
      return response.data;
    } catch (error) {
      console.error('上传文档失败:', error);
      throw error;
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return { documents, loading, fetchDocuments, uploadDocument };
}
```
