from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dependencies import get_database
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse

router = APIRouter(prefix="/search", tags=["搜索"])


@router.get("/", response_model=List[DocumentResponse])
def search_documents(
    keyword: Optional[str] = Query(None, description="搜索关键词"),
    tag_ids: Optional[str] = Query(None, description="标签ID，逗号分隔"),
    file_type: Optional[str] = Query(None, description="文件类型"),
    db: Session = Depends(get_database),
):
    """
    搜索文档
    
    - **keyword**: 搜索关键词（文件名、原始文件名、描述）
    - **tag_ids**: 标签ID，逗号分隔
    - **file_type**: 文件类型过滤
    """
    service = DocumentService(db)
    
    # 解析标签ID
    tag_id_list = None
    if tag_ids:
        tag_id_list = [int(tid) for tid in tag_ids.split(",") if tid.strip()]
    
    return service.search_documents(
        keyword=keyword,
        tag_ids=tag_id_list,
        file_type=file_type,
    )

