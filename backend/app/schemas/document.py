from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

from app.schemas.tag import TagResponse


class DocumentBase(BaseModel):
    """文档基础模式"""
    
    description: Optional[str] = Field(None, description="文档描述")


class DocumentCreate(DocumentBase):
    """创建文档模式"""
    
    tag_ids: Optional[List[int]] = Field(default_factory=list, description="标签ID列表")


class DocumentUpdate(BaseModel):
    """更新文档模式"""
    
    description: Optional[str] = Field(None, description="文档描述")
    tag_ids: Optional[List[int]] = Field(None, description="标签ID列表")


class DocumentResponse(DocumentBase):
    """文档响应模式"""
    
    id: int
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str
    upload_time: datetime
    tags: List[TagResponse] = Field(default_factory=list)
    
    class Config:
        from_attributes = True

