from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from typing import List

from app.core.config import settings
from app.core.exceptions import PDFGenerationError, DocumentNotFoundError
from app.repositories.document_repository import DocumentRepository
from PyPDF2 import PdfMerger


class PDFService:
    """PDF 服务类"""
    
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.db = db
    
    def generate_pdf(
        self,
        document_ids: List[int],
        title: str = "文档汇编",
    ) -> Path:
        """
        生成 PDF 汇编
        
        Args:
            document_ids: 文档ID列表
            title: PDF 标题
            
        Returns:
            Path: 生成的 PDF 文件路径
            
        Raises:
            PDFGenerationError: PDF 生成失败时抛出
        """
        try:
            # 获取所有文档
            documents = []
            for doc_id in document_ids:
                document = self.repository.get_by_id(doc_id)
                if not document:
                    raise DocumentNotFoundError(doc_id)
                documents.append(document)
            
            # 过滤出 PDF 文件
            pdf_documents = [
                doc for doc in documents
                if doc.file_type == "application/pdf"
            ]
            
            if not pdf_documents:
                raise PDFGenerationError("所选文档中没有 PDF 文件")
            
            # 创建 PDF 合并器
            merger = PdfMerger()
            
            # 添加所有 PDF 文件
            for doc in pdf_documents:
                file_path = Path(doc.save_path)
                if file_path.exists():
                    merger.append(str(file_path))
                else:
                    raise PDFGenerationError(f"文件不存在: {doc.save_path}")
            
            # 生成输出文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{title}_{timestamp}.pdf"
            output_path = settings.pdf_output_dir_path / output_filename
            
            # 保存合并后的 PDF
            merger.write(str(output_path))
            merger.close()
            
            return output_path
        except Exception as e:
            if isinstance(e, (PDFGenerationError, DocumentNotFoundError)):
                raise
            raise PDFGenerationError(str(e))

