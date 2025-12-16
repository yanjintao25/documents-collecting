from sqlalchemy.orm import Session
from fastapi import UploadFile
from pathlib import Path
from datetime import datetime
from typing import List, Optional
import asyncio
import logging

from app.core.config import settings
from app.core.exceptions import DocumentNotFoundError, FileNotFoundError
from app.repositories.document_repository import DocumentRepository
from app.schemas.document import DocumentCreate, DocumentUpdate, DocumentResponse
from app.models.document_model import Document

logger = logging.getLogger(__name__)


class DocumentService:
    """文档服务类"""
    
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.db = db
    
    def _document_to_response(self, document: Document, tags: List = None) -> DocumentResponse:
        """
        将数据库文档模型转换为响应对象
        只包含客户端需要的字段，排除内部字段（如 delete_flag, save_path 等）
        """
        from app.schemas.tag import TagResponse
        
        tag_list = [TagResponse.model_validate(tag) for tag in (tags or [])]
        
        return DocumentResponse(
            id=document.id,
            title=document.title,
            file_size=document.file_size,
            file_type=document.file_type,
            pdf_file_size=document.pdf_file_size,
            introduction=document.introduction,
            write_time=document.write_time,
            status=document.status,
            upload_user_name=document.upload_user_name,
            upload_user_id=document.upload_user_id,
            update_user_name=document.update_user_name,
            update_user_id=document.update_user_id,
            category_id=document.category_id,
            category_name=document.category_name,
            create_time=document.create_time,
            update_time=document.update_time,
            description=document.introduction,  # description 会通过验证器从 introduction 同步
            tags=tag_list,
        )
    
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

        # 启动后台任务：异步转换 PDF
        # 如果文件已经是 PDF，跳过转换
        if file_path.suffix.lower() != '.pdf':
            asyncio.create_task(
                self._convert_and_update_pdf(document.id, file_path)
            )

        return self._document_to_response(document, tags=[])
    
    async def _convert_and_update_pdf(
        self,
        document_id: int,
        file_path: Path,
    ):
        """
        异步转换 PDF 并更新数据库
        
        Args:
            document_id: 文档ID
            file_path: 源文件路径
        """
        try:
            logger.info(f"开始转换 PDF (document_id={document_id}, file={file_path})")
            
            # 导入 PDFService（避免循环导入）
            from app.services.pdf_service import PDFService
            pdf_service = PDFService(self.db)
            
            # 转换 PDF
            pdf_path = await pdf_service.convert_to_pdf(file_path)
            
            if pdf_path and pdf_path.exists():
                # 获取 PDF 文件大小
                pdf_file_size = pdf_path.stat().st_size
                
                # 更新数据库
                updated_document = self.repository.update_pdf_info(
                    document_id=document_id,
                    pdf_file_size=pdf_file_size,
                    pdf_save_path=str(pdf_path),
                )
                
                if updated_document:
                    logger.info(
                        f"PDF 转换成功 (document_id={document_id}, "
                        f"pdf_size={pdf_file_size}, pdf_path={pdf_path})"
                    )
                else:
                    logger.warning(f"PDF 转换成功但更新数据库失败 (document_id={document_id})")
            else:
                logger.warning(f"PDF 转换失败，未生成 PDF 文件 (document_id={document_id})")
                
        except Exception as e:
            # 记录错误日志，但不影响主流程
            logger.error(
                f"PDF 转换失败 (document_id={document_id}): {str(e)}",
                exc_info=True
            )
    
    def get_document(self, document_id: int) -> DocumentResponse:
        """获取文档"""
        document = self.repository.get_by_id(document_id)
        if not document:
            raise DocumentNotFoundError(document_id)
        
        # 获取标签信息
        tags = self.repository.get_document_tags(document_id)
        return self._document_to_response(document, tags=tags)
    
    def get_documents(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DocumentResponse]:
        """获取文档列表"""
        documents = self.repository.get_all(skip=skip, limit=limit)
        result = []
        for doc in documents:
            # 获取标签信息
            tags = self.repository.get_document_tags(doc.id)
            result.append(self._document_to_response(doc, tags=tags))
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
        
        # 获取标签信息
        tags = self.repository.get_document_tags(updated_document.id)
        return self._document_to_response(updated_document, tags=tags)
    
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
            # 获取标签信息
            tags = self.repository.get_document_tags(doc.id)
            result.append(self._document_to_response(doc, tags=tags))
        return result

