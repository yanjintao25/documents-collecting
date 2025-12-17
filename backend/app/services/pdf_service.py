from sqlalchemy.orm import Session
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict
import subprocess
import logging
import asyncio
import os
import shutil

import fitz  # PyMuPDF
from PIL import Image

from app.core.config import settings
from app.core.exceptions import PDFGenerationError, DocumentNotFoundError
from app.repositories.document_repository import DocumentRepository

logger = logging.getLogger(__name__)


class PDFService:
    """PDF 服务类"""
    
    # 支持的图片格式
    SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}
    # 支持的 Office 文档格式（需要 LibreOffice）
    SUPPORTED_OFFICE_FORMATS = {'.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.ods', '.odp', '.rtf'}
    
    def __init__(self, db: Session):
        self.repository = DocumentRepository(db)
        self.db = db
        self._libreoffice_path = None  # 缓存 LibreOffice 路径
    
    def _find_libreoffice_path(self) -> Optional[str]:
        """
        查找 LibreOffice 可执行文件路径
        
        Returns:
            str: LibreOffice 可执行文件路径，如果未找到返回 None
        """
        # 如果已缓存，直接返回
        if self._libreoffice_path:
            return self._libreoffice_path
        
        # 如果配置中指定了路径，使用配置的路径
        if settings.LIBREOFFICE_PATH:
            path = Path(settings.LIBREOFFICE_PATH)
            if path.exists():
                self._libreoffice_path = str(path)
                logger.info(f"使用配置的 LibreOffice 路径: {self._libreoffice_path}")
                return self._libreoffice_path
            else:
                logger.warning(f"配置的 LibreOffice 路径不存在: {settings.LIBREOFFICE_PATH}")
        
        # 尝试在 PATH 中查找
        libreoffice_cmd = shutil.which('libreoffice')
        if libreoffice_cmd:
            self._libreoffice_path = libreoffice_cmd
            logger.info(f"在 PATH 中找到 LibreOffice: {self._libreoffice_path}")
            return self._libreoffice_path
        
        # Windows 上尝试常见安装路径
        if os.name == 'nt':  # Windows
            common_paths = [
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
                r"C:\Program Files\LibreOffice 7\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice 7\program\soffice.exe",
            ]
            
            for path_str in common_paths:
                path = Path(path_str)
                if path.exists():
                    self._libreoffice_path = str(path)
                    logger.info(f"在常见路径找到 LibreOffice: {self._libreoffice_path}")
                    return self._libreoffice_path
        
        # Linux/macOS 上尝试其他可能的位置
        else:
            common_paths = [
                "/usr/bin/libreoffice",
                "/usr/local/bin/libreoffice",
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",  # macOS
            ]
            
            for path_str in common_paths:
                path = Path(path_str)
                if path.exists():
                    self._libreoffice_path = str(path)
                    logger.info(f"在常见路径找到 LibreOffice: {self._libreoffice_path}")
                    return self._libreoffice_path
        
        logger.error("未找到 LibreOffice，请安装 LibreOffice 或在配置中指定路径")
        return None
    
    async def convert_to_pdf(
        self,
        file_path: Path,
        output_dir: Optional[Path] = None,
    ) -> Optional[Path]:
        """
        将文件转换为 PDF
        
        Args:
            file_path: 源文件路径
            output_dir: PDF 输出目录（默认使用配置的 PDF 输出目录）
            
        Returns:
            Path: 生成的 PDF 文件路径，转换失败返回 None
        """
        try:
            if not file_path.exists():
                logger.error(f"文件不存在: {file_path}")
                return None
            
            # 如果已经是 PDF，直接返回
            if file_path.suffix.lower() == '.pdf':
                return file_path
            
            # 确定输出目录
            if output_dir is None:
                output_dir = settings.pdf_output_dir_path
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # 生成输出文件名
            pdf_filename = f"{file_path.stem}.pdf"
            output_path = output_dir / pdf_filename
            
            # 根据文件类型选择转换方法
            file_ext = file_path.suffix.lower()
            
            if file_ext in self.SUPPORTED_IMAGE_FORMATS:
                # 图片转 PDF
                return await self._convert_image_to_pdf(file_path, output_path)
            elif file_ext in self.SUPPORTED_OFFICE_FORMATS:
                # Office 文档转 PDF（使用 LibreOffice）
                return await self._convert_office_to_pdf(file_path, output_dir)
            else:
                logger.warning(f"不支持的文件格式: {file_ext}")
                return None
                
        except Exception as e:
            logger.error(f"PDF 转换失败 ({file_path}): {str(e)}", exc_info=True)
            return None
    
    async def _convert_image_to_pdf(
        self,
        image_path: Path,
        output_path: Path,
    ) -> Path:
        """
        将图片转换为 PDF
        
        Args:
            image_path: 图片文件路径
            output_path: 输出 PDF 路径
            
        Returns:
            Path: 生成的 PDF 文件路径
        """
        # 在线程池中执行，避免阻塞
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._convert_image_to_pdf_sync,
            image_path,
            output_path
        )
    
    def _convert_image_to_pdf_sync(
        self,
        image_path: Path,
        output_path: Path,
    ) -> Path:
        """同步版本的图片转 PDF"""
        try:
            # 使用 PyMuPDF 创建 PDF
            doc = fitz.open()
            
            # 打开图片
            img = Image.open(image_path)
            
            # 创建页面（使用图片尺寸）
            page = doc.new_page(width=img.width, height=img.height)
            
            # 插入图片
            rect = page.rect
            page.insert_image(rect, filename=str(image_path))
            
            # 保存 PDF
            doc.save(str(output_path))
            doc.close()
            
            logger.info(f"图片转 PDF 成功: {image_path} -> {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"图片转 PDF 失败: {str(e)}", exc_info=True)
            raise
    
    async def _convert_office_to_pdf(
        self,
        file_path: Path,
        output_dir: Path,
    ) -> Optional[Path]:
        """
        使用 LibreOffice 将 Office 文档转换为 PDF
        
        Args:
            file_path: Office 文档路径
            output_dir: 输出目录
            
        Returns:
            Path: 生成的 PDF 文件路径
        """
        # 在线程池中执行
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self._convert_office_to_pdf_sync,
            file_path,
            output_dir
        )
    
    def _convert_office_to_pdf_sync(
        self,
        file_path: Path,
        output_dir: Path,
    ) -> Optional[Path]:
        """同步版本的 Office 文档转 PDF"""
        try:
            # 查找 LibreOffice 路径
            libreoffice_path = self._find_libreoffice_path()
            if not libreoffice_path:
                logger.error("LibreOffice 未找到，无法转换 Office 文档")
                return None
            
            # 调用 LibreOffice 命令行转换
            result = subprocess.run(
                [
                    libreoffice_path,
                    '--headless',
                    '--convert-to', 'pdf',
                    '--outdir', str(output_dir),
                    str(file_path)
                ],
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            if result.returncode != 0:
                logger.error(f"LibreOffice 转换失败: {result.stderr}")
                if result.stdout:
                    logger.debug(f"LibreOffice 输出: {result.stdout}")
                return None
            
            # LibreOffice 生成的 PDF 文件名
            pdf_path = output_dir / f"{file_path.stem}.pdf"
            
            if pdf_path.exists():
                logger.info(f"Office 文档转 PDF 成功: {file_path} -> {pdf_path}")
                return pdf_path
            else:
                logger.error(f"PDF 文件未生成: {pdf_path}")
                return None
                
        except subprocess.TimeoutExpired:
            logger.error(f"LibreOffice 转换超时: {file_path}")
            return None
        except FileNotFoundError:
            logger.error("LibreOffice 可执行文件未找到")
            return None
        except Exception as e:
            logger.error(f"Office 文档转 PDF 失败: {str(e)}", exc_info=True)
            return None
    
    def add_header_to_pdf(
        self,
        pdf_path: Path,
        header_text: str,
        output_path: Optional[Path] = None,
        font_size: int = 10,
        header_height: float = 50.0,
    ) -> Path:
        """
        给 PDF 添加页眉
        
        Args:
            pdf_path: PDF 文件路径
            header_text: 页眉文本
            output_path: 输出路径（默认覆盖原文件）
            font_size: 字体大小
            header_height: 页眉高度
            
        Returns:
            Path: 输出 PDF 文件路径
        """
        doc = fitz.open(str(pdf_path))
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            rect = page.rect
            
            # 创建页眉区域
            header_rect = fitz.Rect(0, 0, rect.width, header_height)
            
            # 插入页眉文本（居中）
            page.insert_text(
                (rect.width / 2, header_height / 2),
                header_text,
                fontsize=font_size,
                align=1,  # 1=居中
                color=(0, 0, 0),  # 黑色
            )
            
            # 可选：添加页眉分隔线
            page.draw_line(
                fitz.Point(0, header_height),
                fitz.Point(rect.width, header_height),
                color=(0.5, 0.5, 0.5),  # 灰色
                width=0.5
            )
        
        if output_path is None:
            output_path = pdf_path
        
        doc.save(str(output_path))
        doc.close()
        
        return output_path
    
    def merge_pdfs(
        self,
        pdf_paths: List[Path],
        output_path: Path,
        add_bookmarks: bool = True,
    ) -> Path:
        """
        合并多个 PDF 文件
        
        Args:
            pdf_paths: PDF 文件路径列表
            output_path: 输出 PDF 路径
            add_bookmarks: 是否添加书签（每个 PDF 作为一个书签）
            
        Returns:
            Path: 输出 PDF 文件路径
        """
        merged_doc = fitz.open()
        bookmarks = []
        page_offset = 0
        
        for pdf_path in pdf_paths:
            if not pdf_path.exists():
                raise PDFGenerationError(f"文件不存在: {pdf_path}")
            
            doc = fitz.open(str(pdf_path))
            
            # 添加书签
            if add_bookmarks:
                bookmark_title = pdf_path.stem
                bookmarks.append([
                    1,  # 层级（1=一级）
                    bookmark_title,
                    page_offset + 1  # 页码（从1开始）
                ])
            
            # 插入 PDF
            merged_doc.insert_pdf(doc)
            page_offset += len(doc)
            doc.close()
        
        # 设置书签
        if add_bookmarks and bookmarks:
            merged_doc.set_toc(bookmarks)
        
        merged_doc.save(str(output_path))
        merged_doc.close()
        
        return output_path
    
    def add_bookmarks_to_pdf(
        self,
        pdf_path: Path,
        bookmarks: List[Dict[str, any]],
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        给 PDF 添加书签/目录
        
        Args:
            pdf_path: PDF 文件路径
            bookmarks: 书签列表，格式: [{"title": "第一章", "page": 0, "level": 1}, ...]
            output_path: 输出路径（默认覆盖原文件）
            
        Returns:
            Path: 输出 PDF 文件路径
        """
        doc = fitz.open(str(pdf_path))
        
        # 转换为 PyMuPDF 书签格式
        toc = []
        for bookmark in bookmarks:
            toc.append([
                bookmark.get("level", 1),  # 层级
                bookmark["title"],  # 标题
                bookmark["page"] + 1  # 页码（PyMuPDF 从1开始）
            ])
        
        doc.set_toc(toc)
        
        if output_path is None:
            output_path = pdf_path
        
        doc.save(str(output_path))
        doc.close()
        
        return output_path
    
    def generate_pdf(
        self,
        document_ids: List[int],
        title: str = "文档汇编",
        add_header: bool = False,
        header_text: Optional[str] = None,
    ) -> Path:
        """
        生成 PDF 汇编（保留原有接口，使用 PyMuPDF 重构）
        
        Args:
            document_ids: 文档ID列表
            title: PDF 标题
            add_header: 是否添加页眉
            header_text: 页眉文本（如果 add_header=True）
            
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
            
            # 优先使用 PDF 文件，如果没有则使用原始文件
            pdf_paths = []
            for doc in documents:
                file_path = Path(doc.save_path)
                if not file_path.exists():
                    raise PDFGenerationError(f"文件不存在: {doc.save_path}")
                
                # 如果文档有 PDF 版本，优先使用
                if doc.pdf_save_path and Path(doc.pdf_save_path).exists():
                    pdf_paths.append(Path(doc.pdf_save_path))
                elif file_path.suffix.lower() == '.pdf':
                    pdf_paths.append(file_path)
                else:
                    # 如果不是 PDF，尝试转换（同步转换，因为这是同步方法）
                    logger.warning(f"文档 {doc.id} 不是 PDF，跳过合并: {file_path}")
            
            if not pdf_paths:
                raise PDFGenerationError("所选文档中没有可用的 PDF 文件")
            
            # 生成输出文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{title}_{timestamp}.pdf"
            # 使用汇编目录存储汇编PDF（不保存到数据库，仅生成文件）
            output_path = settings.pdf_compilation_dir_path / output_filename
            
            # 合并 PDF
            self.merge_pdfs(
                pdf_paths=pdf_paths,
                output_path=output_path,
                add_bookmarks=True,
            )
            
            # 如果需要，添加页眉
            if add_header and header_text:
                self.add_header_to_pdf(
                    pdf_path=output_path,
                    header_text=header_text or title,
                    output_path=output_path,
                )
            
            return output_path
            
        except Exception as e:
            if isinstance(e, (PDFGenerationError, DocumentNotFoundError)):
                raise
            raise PDFGenerationError(str(e))
