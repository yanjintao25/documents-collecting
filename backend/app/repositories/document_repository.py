from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from pathlib import Path

from app.models.document_model import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


class DocumentRepository:
    """文档仓库类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(
        self,
        filename: str,
        original_filename: str,
        file_path: str,
        file_size: int,
        file_type: str,
        description: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
    ) -> Document:
        """
        创建文档
        
        Args:
            filename: 存储文件名
            original_filename: 原始文件名
            file_path: 文件路径
            file_size: 文件大小
            file_type: 文件类型
            description: 描述
            tag_ids: 标签ID列表
            
        Returns:
            Document: 创建的文档对象
        """
        document = Document(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            description=description,
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        # 通过关系表添加标签关联
        if tag_ids:
            from app.models.document_model import document_tags
            for tag_id in tag_ids:
                self.db.execute(
                    document_tags.insert().values(document_id=document.id, tag_id=tag_id)
                )
            self.db.commit()
        
        return document
    
    def get_by_id(self, document_id: int) -> Optional[Document]:
        """通过ID获取文档"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def get_document_tags(self, document_id: int) -> List:
        """获取文档的标签列表"""
        from app.models.document_model import document_tags
        from app.models.tag_model import Tag
        
        return (
            self.db.query(Tag)
            .join(document_tags, Tag.id == document_tags.c.tag_id)
            .filter(document_tags.c.document_id == document_id)
            .all()
        )
    
    def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Document]:
        """获取所有文档"""
        return self.db.query(Document).offset(skip).limit(limit).all()
    
    def update(
        self,
        document: Document,
        update_data: DocumentUpdate,
    ) -> Document:
        """更新文档"""
        if update_data.description is not None:
            document.description = update_data.description
        
        if update_data.tag_ids is not None:
            from app.models.document_model import document_tags
            # 删除旧的标签关联
            self.db.execute(
                document_tags.delete().where(document_tags.c.document_id == document.id)
            )
            # 添加新的标签关联
            for tag_id in update_data.tag_ids:
                self.db.execute(
                    document_tags.insert().values(document_id=document.id, tag_id=tag_id)
                )
        
        self.db.commit()
        self.db.refresh(document)
        return document
    
    def delete(self, document: Document) -> None:
        """删除文档"""
        # 删除文件
        file_path = Path(document.file_path)
        if file_path.exists():
            file_path.unlink()
        
        self.db.delete(document)
        self.db.commit()
    
    def search(
        self,
        keyword: Optional[str] = None,
        tag_ids: Optional[List[int]] = None,
        file_type: Optional[str] = None,
    ) -> List[Document]:
        """搜索文档"""
        query = self.db.query(Document)
        
        if keyword:
            keyword_filter = or_(
                Document.filename.contains(keyword),
                Document.original_filename.contains(keyword),
                Document.description.contains(keyword),
            )
            query = query.filter(keyword_filter)
        
        if tag_ids:
            from app.models.document_model import document_tags
            query = query.join(document_tags, Document.id == document_tags.c.document_id).filter(
                document_tags.c.tag_id.in_(tag_ids)
            )
        
        if file_type:
            query = query.filter(Document.file_type.contains(file_type))
        
        return query.distinct().all()

