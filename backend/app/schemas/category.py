from pydantic import BaseModel, Field
from datetime import datetime

class CategoryBase(BaseModel):
    """分类基础模式"""

    name: str = Field(..., description="分类名称", min_length=1, max_length=100)

class CategoryCreate(CategoryBase):
    """创建分类模式"""
    pass

class CategoryUpdate(CategoryBase):
    """更新分类模式"""
    pass

class CategoryResponse(CategoryBase):
    """分类响应模式"""
    
    id: int
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    status: int = Field(..., description="状态：0-禁用，1-启用")
    
    class Config:
        from_attributes = True