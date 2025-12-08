from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.core.database import Base
from app.models.base import BaseModel
from app.models.document import document_tags


class Tag(BaseModel):
    """标签模型"""
    
    __tablename__ = "tags"
    
    name = Column(String, unique=True, index=True, nullable=False, comment="标签名称")
    color = Column(String, default="#409EFF", nullable=False, comment="标签颜色")
    
    # 多对多关系：标签可以关联多个文档
    documents = relationship(
        "Document",
        secondary=document_tags,
        back_populates="tags",
        lazy="selectin",
    )

