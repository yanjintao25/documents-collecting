# Categories API 接口调用文档

本文档详细说明了 `categories.py` 中各个接口的调用方法和用例。

**基础URL**: `/api/v1/categories`

---

## 1. 创建分类

### 接口信息
- **方法**: `POST`
- **路径**: `/api/v1/categories/`
- **状态码**: `201 Created`
- **描述**: 创建一个新的分类

### 请求参数
**请求体 (JSON)**:
```json
{
  "name": "分类名称"  // 必填，字符串，长度1-100字符
}
```

### 响应格式
```json
{
  "id": 1,
  "name": "分类名称",
  "create_time": "2024-01-01T12:00:00",
  "update_time": "2024-01-01T12:00:00",
  "status": 1
}
```

### 调用示例

#### cURL
```bash
curl -X POST "http://localhost:8000/api/v1/categories/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "技术文档"
  }'
```

#### Python (requests)
```python
import requests

url = "http://localhost:8000/api/v1/categories/"
data = {
    "name": "技术文档"
}

response = requests.post(url, json=data)
print(response.status_code)  # 201
print(response.json())
# {
#   "id": 1,
#   "name": "技术文档",
#   "create_time": "2024-01-01T12:00:00",
#   "update_time": "2024-01-01T12:00:00",
#   "status": 1
# }
```

#### JavaScript (fetch)
```javascript
fetch('http://localhost:8000/api/v1/categories/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '技术文档'
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
    response = await client.post(
        "http://localhost:8000/api/v1/categories/",
        json={"name": "技术文档"}
    )
    print(response.status_code)  # 201
    print(response.json())
```

### 错误情况
- **400 Bad Request**: 请求参数验证失败（如name为空或超过100字符）
- **409 Conflict**: 分类名称已存在

---

## 2. 获取所有分类

### 接口信息
- **方法**: `GET`
- **路径**: `/api/v1/categories/`
- **状态码**: `200 OK`
- **描述**: 获取所有分类列表

### 请求参数
无

### 响应格式
```json
[
  {
    "id": 1,
    "name": "技术文档",
    "create_time": "2024-01-01T12:00:00",
    "update_time": "2024-01-01T12:00:00",
    "status": 1
  },
  {
    "id": 2,
    "name": "业务文档",
    "create_time": "2024-01-01T13:00:00",
    "update_time": "2024-01-01T13:00:00",
    "status": 1
  }
]
```

### 调用示例

#### cURL
```bash
curl -X GET "http://localhost:8000/api/v1/categories/"
```

#### Python (requests)
```python
import requests

url = "http://localhost:8000/api/v1/categories/"
response = requests.get(url)
print(response.status_code)  # 200
print(response.json())
# [
#   {
#     "id": 1,
#     "name": "技术文档",
#     "create_time": "2024-01-01T12:00:00",
#     "update_time": "2024-01-01T12:00:00",
#     "status": 1
#   },
#   ...
# ]
```

#### JavaScript (fetch)
```javascript
fetch('http://localhost:8000/api/v1/categories/')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    response = await client.get("http://localhost:8000/api/v1/categories/")
    print(response.status_code)  # 200
    print(response.json())
```

---

## 3. 获取单个分类

### 接口信息
- **方法**: `GET`
- **路径**: `/api/v1/categories/{category_id}`
- **状态码**: `200 OK`
- **描述**: 根据ID获取单个分类的详细信息

### 请求参数
**路径参数**:
- `category_id` (int): 分类ID，必填

### 响应格式
```json
{
  "id": 1,
  "name": "技术文档",
  "create_time": "2024-01-01T12:00:00",
  "update_time": "2024-01-01T12:00:00",
  "status": 1
}
```

### 调用示例

#### cURL
```bash
curl -X GET "http://localhost:8000/api/v1/categories/1"
```

#### Python (requests)
```python
import requests

category_id = 1
url = f"http://localhost:8000/api/v1/categories/{category_id}"
response = requests.get(url)
print(response.status_code)  # 200
print(response.json())
# {
#   "id": 1,
#   "name": "技术文档",
#   "create_time": "2024-01-01T12:00:00",
#   "update_time": "2024-01-01T12:00:00",
#   "status": 1
# }
```

#### JavaScript (fetch)
```javascript
const categoryId = 1;
fetch(`http://localhost:8000/api/v1/categories/${categoryId}`)
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    category_id = 1
    response = await client.get(f"http://localhost:8000/api/v1/categories/{category_id}")
    print(response.status_code)  # 200
    print(response.json())
```

### 错误情况
- **404 Not Found**: 分类不存在

---

## 4. 更新分类

### 接口信息
- **方法**: `PUT`
- **路径**: `/api/v1/categories/{category_id}`
- **状态码**: `200 OK`
- **描述**: 更新指定分类的信息

### 请求参数
**路径参数**:
- `category_id` (int): 分类ID，必填

**请求体 (JSON)**:
```json
{
  "name": "新的分类名称"  // 必填，字符串，长度1-100字符
}
```

### 响应格式
```json
{
  "id": 1,
  "name": "新的分类名称",
  "create_time": "2024-01-01T12:00:00",
  "update_time": "2024-01-01T14:00:00",
  "status": 1
}
```

### 调用示例

#### cURL
```bash
curl -X PUT "http://localhost:8000/api/v1/categories/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "更新的分类名称"
  }'
```

#### Python (requests)
```python
import requests

category_id = 1
url = f"http://localhost:8000/api/v1/categories/{category_id}"
data = {
    "name": "更新的分类名称"
}

response = requests.put(url, json=data)
print(response.status_code)  # 200
print(response.json())
# {
#   "id": 1,
#   "name": "更新的分类名称",
#   "create_time": "2024-01-01T12:00:00",
#   "update_time": "2024-01-01T14:00:00",
#   "status": 1
# }
```

#### JavaScript (fetch)
```javascript
const categoryId = 1;
fetch(`http://localhost:8000/api/v1/categories/${categoryId}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: '更新的分类名称'
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
    category_id = 1
    response = await client.put(
        f"http://localhost:8000/api/v1/categories/{category_id}",
        json={"name": "更新的分类名称"}
    )
    print(response.status_code)  # 200
    print(response.json())
```

### 错误情况
- **400 Bad Request**: 请求参数验证失败
- **404 Not Found**: 分类不存在
- **409 Conflict**: 新分类名称已存在

---

## 5. 删除分类

### 接口信息
- **方法**: `DELETE`
- **路径**: `/api/v1/categories/{category_id}`
- **状态码**: `204 No Content`
- **描述**: 删除指定的分类

### 请求参数
**路径参数**:
- `category_id` (int): 分类ID，必填

### 响应格式
无响应体（204状态码）

### 调用示例

#### cURL
```bash
curl -X DELETE "http://localhost:8000/api/v1/categories/1"
```

#### Python (requests)
```python
import requests

category_id = 1
url = f"http://localhost:8000/api/v1/categories/{category_id}"
response = requests.delete(url)
print(response.status_code)  # 204
# 无响应体
```

#### JavaScript (fetch)
```javascript
const categoryId = 1;
fetch(`http://localhost:8000/api/v1/categories/${categoryId}`, {
  method: 'DELETE'
})
  .then(response => {
    if (response.status === 204) {
      console.log('分类删除成功');
    }
  })
  .catch(error => console.error('Error:', error));
```

#### Python (httpx)
```python
import httpx

async with httpx.AsyncClient() as client:
    category_id = 1
    response = await client.delete(f"http://localhost:8000/api/v1/categories/{category_id}")
    print(response.status_code)  # 204
```

### 错误情况
- **404 Not Found**: 分类不存在

---

## 完整用例示例

### 用例1: 完整的CRUD操作流程

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/categories"

# 1. 创建分类
print("=== 创建分类 ===")
create_response = requests.post(
    f"{BASE_URL}/",
    json={"name": "技术文档"}
)
category = create_response.json()
print(f"创建成功: {category}")
category_id = category["id"]

# 2. 获取所有分类
print("\n=== 获取所有分类 ===")
all_categories = requests.get(f"{BASE_URL}/").json()
print(f"分类列表: {all_categories}")

# 3. 获取单个分类
print("\n=== 获取单个分类 ===")
single_category = requests.get(f"{BASE_URL}/{category_id}").json()
print(f"分类详情: {single_category}")

# 4. 更新分类
print("\n=== 更新分类 ===")
update_response = requests.put(
    f"{BASE_URL}/{category_id}",
    json={"name": "更新的技术文档"}
)
updated_category = update_response.json()
print(f"更新成功: {updated_category}")

# 5. 删除分类
print("\n=== 删除分类 ===")
delete_response = requests.delete(f"{BASE_URL}/{category_id}")
print(f"删除状态码: {delete_response.status_code}")  # 204
```

### 用例2: 错误处理示例

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/categories"

# 创建分类时名称重复
try:
    response = requests.post(
        f"{BASE_URL}/",
        json={"name": "已存在的分类"}
    )
    if response.status_code == 409:
        print("错误: 分类名称已存在")
except Exception as e:
    print(f"请求错误: {e}")

# 获取不存在的分类
try:
    response = requests.get(f"{BASE_URL}/99999")
    if response.status_code == 404:
        print("错误: 分类不存在")
except Exception as e:
    print(f"请求错误: {e}")

# 创建分类时名称为空
try:
    response = requests.post(
        f"{BASE_URL}/",
        json={"name": ""}
    )
    if response.status_code == 422:
        print("错误: 分类名称不能为空")
except Exception as e:
    print(f"请求错误: {e}")
```

### 用例3: 批量操作示例

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/categories"

# 批量创建分类
categories_to_create = [
    {"name": "技术文档"},
    {"name": "业务文档"},
    {"name": "设计文档"},
    {"name": "测试文档"}
]

created_categories = []
for category_data in categories_to_create:
    response = requests.post(f"{BASE_URL}/", json=category_data)
    if response.status_code == 201:
        created_categories.append(response.json())
        print(f"创建成功: {category_data['name']}")

# 批量更新分类
for category in created_categories:
    new_name = f"{category['name']} (已更新)"
    response = requests.put(
        f"{BASE_URL}/{category['id']}",
        json={"name": new_name}
    )
    if response.status_code == 200:
        print(f"更新成功: {new_name}")

# 批量删除分类
for category in created_categories:
    response = requests.delete(f"{BASE_URL}/{category['id']}")
    if response.status_code == 204:
        print(f"删除成功: {category['id']}")
```

---

## 注意事项

1. **基础URL**: 请根据实际部署情况修改 `http://localhost:8000` 为实际的服务器地址
2. **Content-Type**: POST 和 PUT 请求需要设置 `Content-Type: application/json` 头
3. **状态码**: 
   - 创建成功返回 `201`
   - 删除成功返回 `204`（无响应体）
   - 其他成功操作返回 `200`
4. **错误处理**: 建议在实际使用中检查响应状态码并处理错误情况
5. **分类名称唯一性**: 系统不允许创建重复的分类名称
6. **分类名称长度**: 分类名称必须在1-100个字符之间

---

## FastAPI 自动文档

FastAPI 提供了自动生成的交互式API文档，可以通过以下地址访问：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

在这些文档中，你可以直接测试所有接口，无需编写代码。
