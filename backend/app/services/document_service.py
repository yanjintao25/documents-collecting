from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
from datetime import datetime
from typing import List, Optional

from app.core.config import settings
from app.core.exceptions import DocumentNotFoundError, FileNotFoundError
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse


class DocumentService:
    """文档服务类"""
    
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.db = db
    
    def upload_document(
        self,
        file: UploadFile,
        description: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
    ) -> DocumentResponse:
        """
        上传文档
        
        Args:
            file: 上传的文件
            description: 文档描述
            tag_ids: 标签ID列表
            
        Returns:
            DocumentResponse: 文档响应对象
        """
        # 生成唯一文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        file_path = settings.upload_dir_path / filename
        
        # 保存文件
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        # 获取文件大小
        file_size = file_path.stat().st_size
        
        # 创建文档记录
        document = self.repository.create(
            filename=filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=file_size,
            file_type=file.content_type or "application/octet-stream",
            description=description,
            tag_ids=tag_ids,
        )
        
        return DocumentResponse.model_validate(document)
    
    def get_document(self, document_id: int) -> DocumentResponse:
        """获取文档"""
        document = self.repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        return DocumentResponse.model_validate(document)
    
    def get_documents(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DocumentResponse]:
        """获取文档列表"""
        documents = self.repository.get_all(skip=skip, limit=limit)
        return [DocumentResponse.model_validate(doc) for doc in documents]
    
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
        return DocumentResponse.model_validate(updated_document)
    
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
        
        file_path = Path(document.file_path)
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
        return [DocumentResponse.model_validate(doc) for doc in documents]

