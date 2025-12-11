"""
快速测试 /api/v1/documents/upload 接口的脚本
使用方法: python tests/test_upload_quick.py
或者从backend目录运行: python -m tests.test_upload_quick
"""
import requests
from pathlib import Path
from io import BytesIO

# 配置
BASE_URL = "http://localhost:8000"
UPLOAD_ENDPOINT = f"{BASE_URL}/api/v1/documents/upload"


def test_upload_file_only():
    """测试1: 仅上传文件"""
    print("\n=== 测试1: 仅上传文件 ===")
    
    # 创建测试文件内容
    file_content = b"This is a test file content."
    files = {
        "file": ("test.txt", BytesIO(file_content), "text/plain")
    }
    
    try:
        response = requests.post(UPLOAD_ENDPOINT, files=files)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            data = response.json()
            print("✅ 上传成功!")
            print(f"文档ID: {data['id']}")
            print(f"文件名: {data['filename']}")
            print(f"原始文件名: {data['original_filename']}")
            print(f"文件大小: {data['file_size']} 字节")
            print(f"文件类型: {data['file_type']}")
            return data['id']
        else:
            print(f"❌ 上传失败: {response.text}")
            return None
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器，请确保后端服务已启动")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def test_upload_with_description():
    """测试2: 上传文件 + 描述"""
    print("\n=== 测试2: 上传文件 + 描述 ===")
    
    file_content = b"Test document with description."
    files = {
        "file": ("document.pdf", BytesIO(file_content), "application/pdf")
    }
    data = {
        "description": "这是一个测试文档，包含描述信息"
    }
    
    try:
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 上传成功!")
            print(f"描述: {result['description']}")
            return result['id']
        else:
            print(f"❌ 上传失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def test_upload_with_tags(tag_ids="1,2"):
    """测试3: 上传文件 + 标签"""
    print(f"\n=== 测试3: 上传文件 + 标签 (tag_ids={tag_ids}) ===")
    
    file_content = b"Test document with tags."
    files = {
        "file": ("tagged.pdf", BytesIO(file_content), "application/pdf")
    }
    data = {
        "tag_ids": tag_ids
    }
    
    try:
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 上传成功!")
            print(f"关联标签数量: {len(result['tags'])}")
            if result['tags']:
                for tag in result['tags']:
                    print(f"  - {tag['name']} (ID: {tag['id']})")
            else:
                print("  ⚠️  未关联任何标签（可能标签ID不存在）")
            return result['id']
        else:
            print(f"❌ 上传失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def test_upload_complete():
    """测试4: 完整测试（文件 + 描述 + 标签）"""
    print("\n=== 测试4: 完整测试（文件 + 描述 + 标签） ===")
    
    file_content = b"Complete test document."
    files = {
        "file": ("complete.pdf", BytesIO(file_content), "application/pdf")
    }
    data = {
        "description": "完整测试：包含描述和标签",
        "tag_ids": "1"
    }
    
    try:
        response = requests.post(UPLOAD_ENDPOINT, files=files, data=data)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 201:
            result = response.json()
            print("✅ 上传成功!")
            print(f"描述: {result['description']}")
            print(f"标签数量: {len(result['tags'])}")
            return result['id']
        else:
            print(f"❌ 上传失败: {response.text}")
            return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None


def test_upload_missing_file():
    """测试5: 缺少文件参数（应该失败）"""
    print("\n=== 测试5: 缺少文件参数（应该失败） ===")
    
    try:
        response = requests.post(UPLOAD_ENDPOINT)
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 422:
            print("✅ 正确返回 422 错误（缺少必需参数）")
        else:
            print(f"⚠️  预期 422，实际返回: {response.status_code}")
    except Exception as e:
        print(f"❌ 错误: {e}")


def check_server():
    """检查服务器是否运行"""
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ 服务器运行正常")
            return True
        else:
            print("⚠️  服务器响应异常")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到服务器")
        print(f"   请确保后端服务运行在 {BASE_URL}")
        return False
    except Exception as e:
        print(f"❌ 检查服务器时出错: {e}")
        return False


def main():
    """主函数"""
    print("=" * 50)
    print("文档上传接口快速测试")
    print("=" * 50)
    
    # 检查服务器
    if not check_server():
        print("\n请先启动后端服务:")
        print("  uvicorn app.main:app --reload")
        return
    
    # 运行测试
    test_upload_file_only()
    test_upload_with_description()
    test_upload_with_tags()
    test_upload_complete()
    test_upload_missing_file()
    
    print("\n" + "=" * 50)
    print("测试完成!")
    print("=" * 50)
    print("\n提示:")
    print("- 访问 http://localhost:8000/docs 查看 Swagger UI")
    print("- 访问 http://localhost:8000/api/v1/documents/ 查看上传的文档列表")


if __name__ == "__main__":
    main()

