from pydantic import BaseModel, Field, model_validator
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
    """文档响应模式 - 只包含客户端需要的字段"""
    
    id: int
    title: str = Field(..., description="文件标题")
    file_size: int = Field(..., description="文件大小")
    file_type: str = Field(..., description="文件类型")
    pdf_file_size: int = Field(..., description="PDF文件大小")
    introduction: Optional[str] = Field(None, description="文章简介")
    write_time: Optional[datetime] = Field(None, description="写作时间")
    status: int = Field(..., description="状态：0-草稿，1-已发布，2-隐藏")
    upload_user_name: str = Field(..., description="上传用户")
    upload_user_id: str = Field(..., description="上传用户ID")
    update_user_name: Optional[str] = Field(None, description="最后更新用户")
    update_user_id: Optional[str] = Field(None, description="最后更新用户ID")
    category_id: Optional[int] = Field(None, description="分类ID")
    category_name: Optional[str] = Field(None, description="分类名称")
    create_time: datetime = Field(..., description="创建时间")
    update_time: datetime = Field(..., description="更新时间")
    # tags 不在数据库模型中，是通过关系查询得到的
    tags: List[TagResponse] = Field(default_factory=list, description="标签列表")
    
    @model_validator(mode='after')
    def set_description_from_introduction(self):
        """将 introduction 的值同步到 description（如果 description 为空）"""
        if self.introduction is not None and self.description is None:
            self.description = self.introduction
        return self
    
    class Config:
        from_attributes = True

