from pydantic import BaseModel, Field
from typing import List, Optional

from app.schemas.document import DocumentResponse


class SearchQuery(BaseModel):
    """搜索查询模式"""
    
    keyword: Optional[str] = Field(None, description="搜索关键词")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID列表")
    file_type: Optional[str] = Field(None, description="文件类型")


class SearchResponse(BaseModel):
    """搜索响应模式"""
    
    total: int = Field(..., description="结果总数")
    documents: List[DocumentResponse] = Field(default_factory=list, description="文档列表")

