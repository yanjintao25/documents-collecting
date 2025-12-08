from pydantic import BaseModel, Field
from datetime import datetime


class TagBase(BaseModel):
    """标签基础模式"""
    
    name: str = Field(..., description="标签名称", min_length=1, max_length=50)
    color: str = Field(default="#409EFF", description="标签颜色")


class TagCreate(TagBase):
    """创建标签模式"""
    pass


class TagUpdate(TagBase):
    """更新标签模式"""
    pass


class TagResponse(TagBase):
    """标签响应模式"""
    
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

