from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Generator

from app.core.database import get_db
from app.models.document import Document
from app.models.tag import Tag


def get_database() -> Generator[Session, None, None]:
    """
    获取数据库会话依赖
    
    Yields:
        Session: 数据库会话
    """
    yield from get_db()


def get_document_by_id(
    document_id: int,
    db: Session = Depends(get_database),
) -> Document:
    """
    通过 ID 获取文档依赖
    
    Args:
        document_id: 文档 ID
        db: 数据库会话
        
    Returns:
        Document: 文档对象
        
    Raises:
        HTTPException: 文档不存在时抛出
    """
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"文档 ID {document_id} 不存在",
        )
    return document


def get_tag_by_id(
    tag_id: int,
    db: Session = Depends(get_database),
) -> Tag:
    """
    通过 ID 获取标签依赖
    
    Args:
        tag_id: 标签 ID
        db: 数据库会话
        
    Returns:
        Tag: 标签对象
        
    Raises:
        HTTPException: 标签不存在时抛出
    """
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"标签 ID {tag_id} 不存在",
        )
    return tag

