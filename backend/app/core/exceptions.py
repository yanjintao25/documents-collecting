from fastapi import HTTPException, status
from typing import Any, Dict, Optional


class BaseAPIException(HTTPException):
    """基础 API 异常类"""
    
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class DocumentNotFoundError(BaseAPIException):
    """文档不存在异常"""
    
    def __init__(self, document_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文档 ID {document_id} 不存在",
        )


class TagNotFoundError(BaseAPIException):
    """标签不存在异常"""
    
    def __init__(self, tag_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"标签 ID {tag_id} 不存在",
        )


class TagAlreadyExistsError(BaseAPIException):
    """标签已存在异常"""
    
    def __init__(self, tag_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"标签 '{tag_name}' 已存在",
        )


class FileNotFoundError(BaseAPIException):
    """文件不存在异常"""
    
    def __init__(self, file_path: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文件不存在: {file_path}",
        )


class PDFGenerationError(BaseAPIException):
    """PDF 生成异常"""
    
    def __init__(self, message: str) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"PDF 生成失败: {message}",
        )

class CategoryNotFoundError(BaseAPIException):
    """分类不存在异常"""
    
    def __init__(self, category_id: int) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"分类 ID {category_id} 不存在",
        )


class CategoryAlreadyExistsError(BaseAPIException):
    """分类已存在异常"""
    
    def __init__(self, category_name: str) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"分类 '{category_name}' 已存在",
        )