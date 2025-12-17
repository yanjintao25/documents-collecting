# PDF API 接口调用文档

本文档详细说明了 `pdf.py` 中各个接口的调用方法和用例。

**基础URL**: `/api/v1/pdf`

---

## 1. 生成文档汇编 PDF

### 接口信息
- **方法**: `POST`
- **路径**: `/api/v1/pdf/generate`
- **状态码**: `200 OK`
- **描述**: 根据指定的文档ID列表生成一个PDF汇编文件
- **Content-Type**: `application/pdf`（响应）

### 请求参数
**请求体 (JSON)**:
```json
{
  "document_ids": [1, 2, 3],  // 必填，文档ID列表，至少包含1个ID
  "title": "文档汇编"  // 可选，PDF标题，默认为"文档汇编"
}
```

### 响应格式
PDF文件流（二进制数据）

### 调用示例

#### cURL
```bash
# 基本生成（使用默认标题）
curl -X POST "http://localhost:8000/api/v1/pdf/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": [1, 2, 3]
  }' \
  -o "generated_pdf.pdf"

# 指定标题
curl -X POST "http://localhost:8000/api/v1/pdf/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "document_ids": [1, 2, 3],
    "title": "2024年度技术文档汇编"
  }' \
  -o "generated_pdf.pdf"
```

#### Python (requests)
```python
import requests

url = "http://localhost:8000/api/v1/pdf/generate"

# 基本生成（使用默认标题）
data = {
    "document_ids": [1, 2, 3]
}
response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    with open("generated_pdf.pdf", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("PDF生成成功")
else:
    print(f"生成失败: {response.status_code}")

# 指定标题
data = {
    "document_ids": [1, 2, 3],
    "title": "2024年度技术文档汇编"
}
response = requests.post(url, json=data, stream=True)

if response.status_code == 200:
    with open("generated_pdf.pdf", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("PDF生成成功")
```

#### JavaScript (fetch)
```javascript
// 基本生成（使用默认标题）
fetch('http://localhost:8000/api/v1/pdf/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    document_ids: [1, 2, 3]
  })
})
  .then(response => {
    if (!response.ok) {
      throw new Error('PDF生成失败');
    }
    return response.blob();
  })
  .then(blob => {
    // 创建下载链接
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated_pdf.pdf';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
  })
  .catch(error => console.error('Error:', error));

// 指定标题
fetch('http://localhost:8000/api/v1/pdf/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    document_ids: [1, 2, 3],
    title: '2024年度技术文档汇编'
  })
})
  .then(response => response.blob())
  .then(blob => {
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'generated_pdf.pdf';
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
    data = {
        "document_ids": [1, 2, 3],
        "title": "2024年度技术文档汇编"
    }
    
    async with client.stream(
        "POST",
        "http://localhost:8000/api/v1/pdf/generate",
        json=data
    ) as response:
        if response.status_code == 200:
            filename = "generated_pdf.pdf"
            with open(filename, "wb") as f:
                async for chunk in response.aiter_bytes():
                    f.write(chunk)
            print(f"PDF生成成功: {filename}")
        else:
            print(f"生成失败: {response.status_code}")
```

### 错误情况
- **400 Bad Request**: 请求参数验证失败（如document_ids为空或包含无效ID）
- **404 Not Found**: 指定的文档ID不存在
- **422 Unprocessable Entity**: 请求参数格式错误（如document_ids不是数组或为空）
- **500 Internal Server Error**: PDF生成过程中出现错误

---

## 完整用例示例

### 用例1: 基本PDF生成

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/pdf"

# 生成包含3个文档的PDF汇编
document_ids = [1, 2, 3]
data = {
    "document_ids": document_ids
}

response = requests.post(f"{BASE_URL}/generate", json=data, stream=True)

if response.status_code == 200:
    with open("document_compilation.pdf", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("PDF生成成功")
else:
    print(f"生成失败: {response.status_code}")
    print(response.text)
```

### 用例2: 指定标题生成PDF

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/pdf"

# 生成指定标题的PDF汇编
document_ids = [1, 2, 3, 4, 5]
data = {
    "document_ids": document_ids,
    "title": "2024年度技术文档汇编"
}

response = requests.post(f"{BASE_URL}/generate", json=data, stream=True)

if response.status_code == 200:
    filename = "2024_tech_docs.pdf"
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f"PDF生成成功: {filename}")
else:
    print(f"生成失败: {response.status_code}")
```

### 用例3: 批量生成多个PDF汇编

```python
import requests
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1/pdf"

# 定义多个文档组合
document_groups = [
    {
        "ids": [1, 2, 3],
        "title": "技术文档汇编_第一册"
    },
    {
        "ids": [4, 5, 6],
        "title": "技术文档汇编_第二册"
    },
    {
        "ids": [7, 8, 9, 10],
        "title": "技术文档汇编_第三册"
    }
]

output_dir = Path("./pdf_outputs")
output_dir.mkdir(exist_ok=True)

for group in document_groups:
    print(f"生成PDF: {group['title']}")
    data = {
        "document_ids": group["ids"],
        "title": group["title"]
    }
    
    response = requests.post(f"{BASE_URL}/generate", json=data, stream=True)
    
    if response.status_code == 200:
        filename = output_dir / f"{group['title']}.pdf"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✓ 生成成功: {filename}")
    else:
        print(f"✗ 生成失败: {group['title']} - {response.status_code}")
```

### 用例4: 根据分类生成PDF汇编

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
PDF_BASE = f"{BASE_URL}/pdf"
DOCUMENTS_BASE = f"{BASE_URL}/documents"

# 1. 获取所有文档
documents_response = requests.get(f"{DOCUMENTS_BASE}/")
all_documents = documents_response.json()

# 2. 按分类分组
documents_by_category = {}
for doc in all_documents:
    category_id = doc.get("category_id")
    if category_id:
        if category_id not in documents_by_category:
            documents_by_category[category_id] = []
        documents_by_category[category_id].append(doc["id"])

# 3. 为每个分类生成PDF
for category_id, doc_ids in documents_by_category.items():
    # 获取分类名称
    category_response = requests.get(f"{BASE_URL}/categories/{category_id}")
    category_name = category_response.json().get("name", f"分类{category_id}")
    
    print(f"为分类 '{category_name}' 生成PDF汇编...")
    
    data = {
        "document_ids": doc_ids,
        "title": f"{category_name}文档汇编"
    }
    
    response = requests.post(f"{PDF_BASE}/generate", json=data, stream=True)
    
    if response.status_code == 200:
        filename = f"{category_name}_汇编.pdf"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"✓ 生成成功: {filename}")
    else:
        print(f"✗ 生成失败: {category_name} - {response.status_code}")
```

### 用例5: 根据标签生成PDF汇编

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"
PDF_BASE = f"{BASE_URL}/pdf"
DOCUMENTS_BASE = f"{DOCUMENTS_BASE}/documents"

# 1. 获取所有文档
documents_response = requests.get(f"{DOCUMENTS_BASE}/")
all_documents = documents_response.json()

# 2. 筛选包含特定标签的文档
target_tag_id = 1  # 例如：标签ID为1的文档
tagged_documents = [
    doc["id"] for doc in all_documents
    if any(tag["id"] == target_tag_id for tag in doc.get("tags", []))
]

if tagged_documents:
    print(f"找到 {len(tagged_documents)} 个包含标签的文档")
    
    data = {
        "document_ids": tagged_documents,
        "title": "重要文档汇编"
    }
    
    response = requests.post(f"{PDF_BASE}/generate", json=data, stream=True)
    
    if response.status_code == 200:
        filename = "important_docs.pdf"
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"PDF生成成功: {filename}")
    else:
        print(f"生成失败: {response.status_code}")
else:
    print("没有找到符合条件的文档")
```

### 用例6: 错误处理示例

```python
import requests

BASE_URL = "http://localhost:8000/api/v1/pdf"

# 测试1: 空的文档ID列表
try:
    data = {"document_ids": []}
    response = requests.post(f"{BASE_URL}/generate", json=data)
    if response.status_code == 422:
        print("错误: 文档ID列表不能为空")
except Exception as e:
    print(f"请求错误: {e}")

# 测试2: 包含不存在的文档ID
try:
    data = {"document_ids": [99999, 99998]}
    response = requests.post(f"{BASE_URL}/generate", json=data)
    if response.status_code == 404:
        print("错误: 指定的文档不存在")
except Exception as e:
    print(f"请求错误: {e}")

# 测试3: 无效的请求格式
try:
    data = {"document_ids": "not_an_array"}
    response = requests.post(f"{BASE_URL}/generate", json=data)
    if response.status_code == 422:
        print("错误: 请求参数格式错误")
except Exception as e:
    print(f"请求错误: {e}")

# 测试4: 正常情况
try:
    data = {"document_ids": [1, 2, 3]}
    response = requests.post(f"{BASE_URL}/generate", json=data, stream=True)
    if response.status_code == 200:
        with open("test_output.pdf", "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("PDF生成成功")
    else:
        print(f"生成失败: {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"请求错误: {e}")
```

### 用例7: 异步批量生成PDF

```python
import asyncio
import httpx
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1/pdf"

async def generate_pdf_async(client, document_ids, title, output_path):
    """异步生成PDF"""
    try:
        data = {
            "document_ids": document_ids,
            "title": title
        }
        
        async with client.stream(
            "POST",
            f"{BASE_URL}/generate",
            json=data,
            timeout=300.0  # 5分钟超时
        ) as response:
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    async for chunk in response.aiter_bytes():
                        f.write(chunk)
                return True, f"生成成功: {output_path}"
            else:
                return False, f"生成失败: {response.status_code}"
    except Exception as e:
        return False, f"错误: {str(e)}"

async def batch_generate_pdfs():
    """批量异步生成PDF"""
    document_groups = [
        {"ids": [1, 2, 3], "title": "汇编1", "file": "compilation_1.pdf"},
        {"ids": [4, 5, 6], "title": "汇编2", "file": "compilation_2.pdf"},
        {"ids": [7, 8, 9], "title": "汇编3", "file": "compilation_3.pdf"},
    ]
    
    async with httpx.AsyncClient() as client:
        tasks = [
            generate_pdf_async(
                client,
                group["ids"],
                group["title"],
                group["file"]
            )
            for group in document_groups
        ]
        
        results = await asyncio.gather(*tasks)
        
        for success, message in results:
            print(message)

# 运行异步任务
asyncio.run(batch_generate_pdfs())
```

---

## 前端集成示例

### Vue 3 + TypeScript 示例

```typescript
// api/pdf.ts
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1/pdf';

export interface PDFGenerateRequest {
  document_ids: number[];
  title?: string;
}

/**
 * 生成PDF汇编
 */
export async function generatePDF(
  request: PDFGenerateRequest
): Promise<Blob> {
  const response = await axios.post(
    `${API_BASE}/generate`,
    request,
    {
      responseType: 'blob',
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data;
}

/**
 * 生成PDF并触发下载
 */
export async function generateAndDownloadPDF(
  request: PDFGenerateRequest
): Promise<void> {
  const blob = await generatePDF(request);
  
  // 创建下载链接
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = request.title 
    ? `${request.title}.pdf` 
    : 'document_compilation.pdf';
  document.body.appendChild(a);
  a.click();
  
  // 清理
  window.URL.revokeObjectURL(url);
  document.body.removeChild(a);
}
```

### Vue 组件使用示例

```vue
<template>
  <div>
    <h2>生成PDF汇编</h2>
    
    <div>
      <label>选择文档:</label>
      <div v-for="doc in documents" :key="doc.id">
        <input
          type="checkbox"
          :value="doc.id"
          v-model="selectedDocumentIds"
        />
        {{ doc.title }}
      </div>
    </div>
    
    <div>
      <label>PDF标题:</label>
      <input v-model="pdfTitle" placeholder="文档汇编" />
    </div>
    
    <button 
      @click="handleGeneratePDF" 
      :disabled="selectedDocumentIds.length === 0 || loading"
    >
      {{ loading ? '生成中...' : '生成PDF' }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { generateAndDownloadPDF } from '@/api/pdf';
import type { PDFGenerateRequest } from '@/types/pdf';

const documents = ref([]); // 从API获取的文档列表
const selectedDocumentIds = ref<number[]>([]);
const pdfTitle = ref('文档汇编');
const loading = ref(false);

const handleGeneratePDF = async () => {
  if (selectedDocumentIds.value.length === 0) {
    alert('请至少选择一个文档');
    return;
  }
  
  loading.value = true;
  try {
    const request: PDFGenerateRequest = {
      document_ids: selectedDocumentIds.value,
      title: pdfTitle.value || '文档汇编',
    };
    
    await generateAndDownloadPDF(request);
    alert('PDF生成成功');
  } catch (error) {
    console.error('PDF生成失败:', error);
    alert('PDF生成失败，请重试');
  } finally {
    loading.value = false;
  }
};
</script>
```

### React 示例

```typescript
// hooks/usePDF.ts
import { useState } from 'react';
import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1/pdf';

export interface PDFGenerateRequest {
  document_ids: number[];
  title?: string;
}

export function usePDF() {
  const [loading, setLoading] = useState(false);

  const generatePDF = async (request: PDFGenerateRequest): Promise<Blob> => {
    const response = await axios.post(
      `${API_BASE}/generate`,
      request,
      {
        responseType: 'blob',
      }
    );
    return response.data;
  };

  const generateAndDownload = async (request: PDFGenerateRequest) => {
    setLoading(true);
    try {
      const blob = await generatePDF(request);
      
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = request.title 
        ? `${request.title}.pdf` 
        : 'document_compilation.pdf';
      document.body.appendChild(a);
      a.click();
      
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('PDF生成失败:', error);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return { generatePDF, generateAndDownload, loading };
}
```

### React 组件使用示例

```tsx
import React, { useState } from 'react';
import { usePDF } from './hooks/usePDF';

function PDFGenerator() {
  const [selectedIds, setSelectedIds] = useState<number[]>([]);
  const [title, setTitle] = useState('文档汇编');
  const { generateAndDownload, loading } = usePDF();

  const handleGenerate = async () => {
    if (selectedIds.length === 0) {
      alert('请至少选择一个文档');
      return;
    }

    try {
      await generateAndDownload({
        document_ids: selectedIds,
        title: title || '文档汇编',
      });
      alert('PDF生成成功');
    } catch (error) {
      alert('PDF生成失败，请重试');
    }
  };

  return (
    <div>
      <h2>生成PDF汇编</h2>
      
      <div>
        <label>PDF标题:</label>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="文档汇编"
        />
      </div>
      
      <button 
        onClick={handleGenerate} 
        disabled={selectedIds.length === 0 || loading}
      >
        {loading ? '生成中...' : '生成PDF'}
      </button>
    </div>
  );
}

export default PDFGenerator;
```

---

## 注意事项

1. **基础URL**: 请根据实际部署情况修改 `http://localhost:8000` 为实际的服务器地址

2. **文档ID列表**:
   - `document_ids` 必须是一个非空数组
   - 至少包含1个文档ID
   - 所有文档ID必须存在，否则会返回404错误

3. **PDF标题**:
   - `title` 参数是可选的
   - 如果不提供，默认使用 "文档汇编"
   - 标题会显示在生成的PDF文件中

4. **响应处理**:
   - 接口返回PDF文件流（二进制数据）
   - Content-Type 为 `application/pdf`
   - 需要使用流式下载处理大文件
   - 建议设置合理的超时时间（PDF生成可能需要较长时间）

5. **性能考虑**:
   - PDF生成是CPU密集型操作，可能需要较长时间
   - 建议为大量文档的PDF生成设置较长的超时时间
   - 可以考虑使用异步请求或后台任务处理

6. **错误处理**:
   - 建议检查响应状态码
   - 处理404（文档不存在）和422（参数验证失败）错误
   - 对于500错误，可能是PDF生成过程中的内部错误

7. **文件下载**:
   - 前端需要正确处理Blob响应
   - 使用 `URL.createObjectURL` 创建下载链接
   - 下载完成后记得释放URL对象

---

## FastAPI 自动文档

FastAPI 提供了自动生成的交互式API文档，可以通过以下地址访问：

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

在这些文档中，你可以直接测试PDF生成接口，但需要注意：
- Swagger UI 可能无法直接下载PDF文件
- 建议使用 Postman 或 curl 等工具测试文件下载功能

---

## 常见问题

### Q1: PDF生成需要多长时间？
A: 生成时间取决于文档数量和大小。通常单个文档需要几秒到几十秒不等。建议设置合理的超时时间（如5分钟）。

### Q2: 可以生成包含多少文档的PDF？
A: 理论上没有限制，但建议：
- 少于50个文档：通常可以正常处理
- 50-100个文档：可能需要较长时间，建议使用异步处理
- 超过100个文档：建议分批生成或优化文档大小

### Q3: 如果某个文档ID不存在会怎样？
A: 接口会返回404错误，整个PDF生成会失败。建议在生成前先验证所有文档ID是否存在。

### Q4: 生成的PDF文件大小有限制吗？
A: 文件大小取决于源文档的大小和数量。如果生成的PDF过大，可能需要考虑：
- 压缩PDF
- 分批生成
- 优化源文档

### Q5: 可以自定义PDF的样式吗？
A: 当前接口不支持自定义样式，PDF样式由服务端决定。如需自定义样式，需要修改服务端代码。
