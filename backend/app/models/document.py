from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.base import BaseModel

# 文档和标签的多对多关系表
document_tags = Table(
    "document_tags",
    Base.metadata,
    Column("document_id", Integer, ForeignKey("documents.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)


class Document(BaseModel):
    """文档模型"""
    
    __tablename__ = "documents"
    
    filename = Column(String, index=True, nullable=False, comment="存储文件名")
    original_filename = Column(String, nullable=False, comment="原始文件名")
    file_path = Column(String, nullable=False, comment="文件存储路径")
    file_size = Column(Integer, nullable=False, comment="文件大小（字节）")
    file_type = Column(String, nullable=False, comment="文件 MIME 类型")
    description = Column(Text, nullable=True, comment="文档描述")
    upload_time = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="上传时间",
    )
    
    # 多对多关系：文档可以有多个标签
    tags = relationship(
        "Tag",
        secondary=document_tags,
        back_populates="documents",
        lazy="selectin",
    )

