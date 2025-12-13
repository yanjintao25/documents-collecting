from sqlalchemy import Column, String, Integer, Text, ForeignKey, Table, DateTime, UniqueConstraint, Index
from sqlalchemy.sql import func

from app.core.database import Base
from app.models.base_model import BaseModel

# 文档和标签的多对多关系表
document_tags = Table(
    "document_tags",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, comment="关联ID"),
    Column("document_id", Integer, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, comment="文件ID"),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False, comment="标签ID"),
    Column("create_time", DateTime(timezone=True), server_default=func.now(), nullable=False, comment="创建时间"),
    UniqueConstraint("document_id", "tag_id", name="uq_document_tags_document_tag", comment="文件和标签组合唯一"),
    Index("idx_document_tags_document_id", "document_id"),
    Index("idx_document_tags_tag_id", "tag_id"),
)


class Document(BaseModel):
    """文档模型"""
    
    __tablename__ = "documents"
    
    title = Column(String(255), nullable=False, comment="文件标题")
    save_path = Column(String(500), nullable=False, comment="文件内容保存路径")
    file_size = Column(Integer, nullable=False, comment="文件大小")
    file_type = Column(String(100), nullable=False, comment="文件类型")
    pdf_file_size = Column(Integer, nullable=False, comment="PDF文件大小")
    pdf_save_path = Column(String(500), nullable=True, comment="PDF文件保存路径")
    introduction = Column(Text, nullable=True, comment="文章简介")
    write_time = Column(DateTime(timezone=True), nullable=True, comment="写作时间")
    status = Column(Integer, nullable=False, default=1, comment="状态：0-草稿，1-已发布，2-隐藏")
    upload_user_name = Column(String(100), nullable=False, comment="上传用户")
    upload_user_id = Column(String(100), nullable=False, comment="上传用户ID")
    update_user_name = Column(String(100), nullable=True, comment="最后更新用户")
    update_user_id = Column(String(100), nullable=True, comment="最后更新用户ID")
    category_id = Column(Integer, nullable=True, comment="分类ID")
    category_name = Column(String(100), nullable=True, comment="分类名称")
    delete_flag = Column(Integer, nullable=False, default=0, comment="删除标志：0-未删除，1-已删除")
    
    __table_args__ = (
        Index("idx_documents_status", "status"),
        Index("idx_documents_category_id", "category_id"),
        Index("idx_documents_delete_flag", "delete_flag"),
        Index("idx_documents_create_time", "create_time"),
        Index("idx_documents_update_time", "update_time"),
    )

