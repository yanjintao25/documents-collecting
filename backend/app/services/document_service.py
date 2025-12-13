from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from app.core.config import settings
from app.core.exceptions import DocumentNotFoundError, FileNotFoundError
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.models.document_model import Document


class DocumentService:
    """文档服务类"""
    
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.db = db
    
    async def upload_document(
        self,
        file: UploadFile,
        description: Optional[str] = None,
        category_id: Optional[int] = None,
    ) -> DocumentResponse:
        """
        上传文档
        
        Args:
            file: 上传的文件
            description: 文档描述
            category_id: 分类ID
            
        Returns:
            DocumentResponse: 文档响应对象
        """
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = settings.upload_dir_path / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # 获取文件大小
        file_size = file_path.stat().st_size
        
        # 查询分类名称（如果提供了分类ID）
        category_name = None
        if category_id:
            from app.models.category_model import Category
            category = self.db.query(Category).filter(
                Category.id == category_id,
                Category.delete_flag == 0
            ).first()
            if category:
                category_name = category.name
        
        # 创建文档记录
        document = self.repository.create(
            title=file.filename,  # 使用原始文件名作为标题
            save_path=str(file_path),
            file_size=file_size,
            file_type=file.content_type or "application/octet-stream",
            introduction=description,
            category_id=category_id,
            category_name=category_name,
        )
        
        # 初始写入的记录不包含标签信息
        tags = self.repository.get_document_tags(document.id)
        document_dict = {
            **{c.name: getattr(document, c.name) for c in document.__table__.columns},
            "tags": tags,
        }
        return DocumentResponse.model_validate(document_dict)
    
    def get_document(self, document_id: int) -> DocumentResponse:
        """获取文档"""
        document = self.repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        
        # 手动添加标签信息
        tags = self.repository.get_document_tags(document_id)
        document_dict = {
            **{c.name: getattr(document, c.name) for c in document.__table__.columns},
            "tags": tags,
        }
        return DocumentResponse.model_validate(document_dict)
    
    def get_documents(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DocumentResponse]:
        """获取文档列表"""
        documents = self.repository.get_all(skip=skip, limit=limit)
        result = []
        for doc in documents:
            # 手动添加标签信息
            tags = self.repository.get_document_tags(doc.id)
            document_dict = {
                **{c.name: getattr(doc, c.name) for c in doc.__table__.columns},
                "tags": tags,
            }
            result.append(DocumentResponse.model_validate(document_dict))
        return result
    
    def update_document(
        self,
        document_id: int,
        update_data: DocumentUpdate,
    ) -> DocumentResponse:
        """更新文档"""
        document = self.repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        
        updated_document = self.repository.update(document, update_data)
        
        # 手动添加标签信息
        tags = self.repository.get_document_tags(updated_document.id)
        document_dict = {
            **{c.name: getattr(updated_document, c.name) for c in updated_document.__table__.columns},
            "tags": tags,
        }
        return DocumentResponse.model_validate(document_dict)
    
    def delete_document(self, document_id: int) -> None:
        """删除文档"""
        document = self.repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        
        self.repository.delete(document)
    
    def get_file_path(self, document_id: int) -> Path:
        """获取文档文件路径"""
        document = self.repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        
        file_path = Path(document.save_path)
        if not file_path.exists():
            raise FileNotFoundError(str(file_path))
        
        return file_path
    
    def search_documents(
        self,
        keyword: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
        file_type: Optional[str] = None,
    ) -> List[DocumentResponse]:
        """搜索文档"""
        documents = self.repository.search(
            keyword=keyword,
            tag_ids=tag_ids,
            file_type=file_type,
        )
        result = []
        for doc in documents:
            # 手动添加标签信息
            tags = self.repository.get_document_tags(doc.id)
            document_dict = {
                **{c.name: getattr(doc, c.name) for c in doc.__table__.columns},
                "tags": tags,
            }
            result.append(DocumentResponse.model_validate(document_dict))
        return result

