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
        title: str,
        save_path: str,
        file_size: int,
        file_type: str,
        introduction: Optional[str] = None,
        category_id: Optional[int] = None,
        category_name: Optional[str] = None,
    ) -> Document:
        """
        创建文档
        
        Args:
            title: 文件标题
            save_path: 文件保存路径
            file_size: 文件大小
            file_type: 文件类型
            introduction: 文章简介
            category_id: 分类ID
            category_name: 分类名称
            
        Returns:
            Document: 创建的文档对象
        """
        document = Document(
            title=title,
            save_path=save_path,
            file_size=file_size,
            file_type=file_type,
            pdf_file_size=0,
            pdf_save_path=None,
            introduction=introduction,
            upload_user_name="默认用户",
            upload_user_id="001",
            category_id=category_id,
            category_name=category_name,
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return document
    
    def get_by_id(self, document_id: int) -> Optional[Document]:
        """通过ID获取文档"""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def update_pdf_info(
        self,
        document_id: int,
        pdf_file_size: int,
        pdf_save_path: str,
    ) -> Optional[Document]:
        """
        更新文档的 PDF 信息
        
        Args:
            document_id: 文档ID
            pdf_file_size: PDF 文件大小
            pdf_save_path: PDF 文件保存路径
            
        Returns:
            Document: 更新后的文档对象，如果文档不存在返回 None
        """
        document = self.get_by_id(document_id)
        if not document:
            return None
        
        document.pdf_file_size = pdf_file_size
        document.pdf_save_path = pdf_save_path
        self.db.commit()
        self.db.refresh(document)
        return document
    
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
        file_path = Path(document.save_path)
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
                Document.title.contains(keyword),
                Document.introduction.contains(keyword),
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

