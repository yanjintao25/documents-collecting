"""
测试 /api/v1/documents/upload 接口
"""
import pytest
from pathlib import Path
from io import BytesIO


class TestDocumentUpload:
    """文档上传接口测试类"""
    
    def test_upload_file_only(self, client, temp_upload_dir, sample_pdf_file):
        """测试1: 仅上传文件（无描述、无标签）"""
        # 准备文件
        files = {
            "file": ("test.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        
        # 发送请求
        response = client.post("/api/v1/documents/upload", files=files)
        
        # 验证响应
        assert response.status_code == 201
        data = response.json()
        
        # 验证响应字段
        assert "id" in data
        assert "filename" in data
        assert "original_filename" in data
        assert data["original_filename"] == "test.pdf"
        assert "file_path" in data
        assert "file_size" in data
        assert data["file_size"] == len(sample_pdf_file)
        assert "file_type" in data
        assert data["file_type"] == "application/pdf"
        assert "upload_time" in data
        assert "tags" in data
        assert data["tags"] == []
        assert data["description"] is None
        
        # 验证文件已保存
        file_path = Path(data["file_path"])
        assert file_path.exists()
        assert file_path.read_bytes() == sample_pdf_file
        
        # 验证文件名格式（包含时间戳）
        assert "_test.pdf" in data["filename"]
    
    def test_upload_file_with_description(self, client, temp_upload_dir, sample_pdf_file):
        """测试2: 上传文件 + 描述"""
        files = {
            "file": ("document.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "description": "这是一个测试文档描述"
        }
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["description"] == "这是一个测试文档描述"
        assert result["original_filename"] == "document.pdf"
    
    def test_upload_file_with_tags(self, client, temp_upload_dir, sample_pdf_file, sample_tag):
        """测试3: 上传文件 + 标签"""
        files = {
            "file": ("tagged.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "tag_ids": str(sample_tag.id)
        }
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert len(result["tags"]) == 1
        assert result["tags"][0]["id"] == sample_tag.id
        assert result["tags"][0]["name"] == sample_tag.name
    
    def test_upload_file_with_multiple_tags(self, client, temp_upload_dir, sample_pdf_file, db_session):
        """测试4: 上传文件 + 多个标签"""
        from app.models.tag_model import Tag
        
        # 创建多个标签
        tag1 = Tag(name="标签1", color="#FF0000")
        tag2 = Tag(name="标签2", color="#00FF00")
        tag3 = Tag(name="标签3", color="#0000FF")
        db_session.add_all([tag1, tag2, tag3])
        db_session.commit()
        
        files = {
            "file": ("multi_tagged.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "tag_ids": f"{tag1.id},{tag2.id},{tag3.id}"
        }
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert len(result["tags"]) == 3
        tag_ids = [tag["id"] for tag in result["tags"]]
        assert tag1.id in tag_ids
        assert tag2.id in tag_ids
        assert tag3.id in tag_ids
    
    def test_upload_file_with_description_and_tags(
        self, client, temp_upload_dir, sample_pdf_file, sample_tag
    ):
        """测试5: 上传文件 + 描述 + 标签"""
        files = {
            "file": ("complete.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "description": "完整测试：包含描述和标签",
            "tag_ids": str(sample_tag.id)
        }
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["description"] == "完整测试：包含描述和标签"
        assert len(result["tags"]) == 1
        assert result["tags"][0]["id"] == sample_tag.id
    
    def test_upload_text_file(self, client, temp_upload_dir, sample_text_file):
        """测试6: 上传文本文件"""
        files = {
            "file": ("test.txt", BytesIO(sample_text_file), "text/plain")
        }
        
        response = client.post("/api/v1/documents/upload", files=files)
        
        assert response.status_code == 201
        result = response.json()
        assert result["file_type"] == "text/plain"
        assert result["original_filename"] == "test.txt"
        assert result["file_size"] == len(sample_text_file)
    
    def test_upload_file_without_content_type(self, client, temp_upload_dir, sample_pdf_file):
        """测试7: 上传文件但未指定 content-type"""
        files = {
            "file": ("unknown.bin", BytesIO(sample_pdf_file))
        }
        
        response = client.post("/api/v1/documents/upload", files=files)
        
        assert response.status_code == 201
        result = response.json()
        # 应该使用默认的 application/octet-stream
        assert result["file_type"] in ["application/octet-stream", "application/pdf"]
    
    def test_upload_missing_file(self, client):
        """测试8: 缺少文件参数（应该失败）"""
        response = client.post("/api/v1/documents/upload")
        
        # FastAPI 应该返回 422 Unprocessable Entity
        assert response.status_code == 422
    
    def test_upload_with_invalid_tag_ids(self, client, temp_upload_dir, sample_pdf_file):
        """测试9: 使用不存在的标签ID（应该成功，但不关联标签）"""
        files = {
            "file": ("test.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "tag_ids": "99999"  # 不存在的标签ID
        }
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        # 注意：当前实现不会报错，只是不关联标签
        assert response.status_code == 201
        result = response.json()
        assert result["tags"] == []
    
    def test_upload_with_empty_tag_ids(self, client, temp_upload_dir, sample_pdf_file):
        """测试10: 空标签ID字符串"""
        files = {
            "file": ("test.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "tag_ids": ""
        }
        
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        assert response.status_code == 201
        result = response.json()
        assert result["tags"] == []
    
    def test_upload_with_whitespace_tag_ids(self, client, temp_upload_dir, sample_pdf_file):
        """测试11: 标签ID包含空格"""
        files = {
            "file": ("test.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        data = {
            "tag_ids": " 1 , 2 , 3 "  # 包含空格
        }
        
        # 应该能正确处理，去除空格
        response = client.post("/api/v1/documents/upload", files=files, data=data)
        
        # 由于标签不存在，tags 应该为空
        assert response.status_code == 201
    
    def test_upload_file_size_calculation(self, client, temp_upload_dir):
        """测试12: 验证文件大小计算正确"""
        # 创建一个特定大小的文件
        file_size = 1024  # 1KB
        file_content = b"x" * file_size
        
        files = {
            "file": ("size_test.bin", BytesIO(file_content), "application/octet-stream")
        }
        
        response = client.post("/api/v1/documents/upload", files=files)
        
        assert response.status_code == 201
        result = response.json()
        assert result["file_size"] == file_size
    
    def test_upload_filename_with_special_characters(self, client, temp_upload_dir, sample_pdf_file):
        """测试13: 文件名包含特殊字符"""
        files = {
            "file": ("测试文档 (1).pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        
        response = client.post("/api/v1/documents/upload", files=files)
        
        assert response.status_code == 201
        result = response.json()
        assert result["original_filename"] == "测试文档 (1).pdf"
        # 验证文件已保存
        file_path = Path(result["file_path"])
        assert file_path.exists()
    
    def test_upload_multiple_files_sequentially(self, client, temp_upload_dir, sample_pdf_file):
        """测试14: 连续上传多个文件，验证ID递增"""
        file_ids = []
        
        for i in range(3):
            files = {
                "file": (f"file_{i}.pdf", BytesIO(sample_pdf_file), "application/pdf")
            }
            response = client.post("/api/v1/documents/upload", files=files)
            assert response.status_code == 201
            file_ids.append(response.json()["id"])
        
        # 验证ID是递增的
        assert file_ids == sorted(file_ids)
        assert len(set(file_ids)) == 3  # 所有ID都是唯一的
    
    def test_upload_file_timestamp_in_filename(self, client, temp_upload_dir, sample_pdf_file):
        """测试15: 验证文件名包含时间戳"""
        from datetime import datetime
        
        files = {
            "file": ("test.pdf", BytesIO(sample_pdf_file), "application/pdf")
        }
        
        response = client.post("/api/v1/documents/upload", files=files)
        
        assert response.status_code == 201
        result = response.json()
        filename = result["filename"]
        
        # 验证文件名格式：YYYYMMDD_HHMMSS_原文件名
        # 提取时间戳部分
        parts = filename.split("_", 2)
        assert len(parts) >= 3
        
        # 验证时间戳格式
        timestamp_str = f"{parts[0]}_{parts[1]}"
        try:
            datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
        except ValueError:
            pytest.fail(f"文件名时间戳格式不正确: {timestamp_str}")
