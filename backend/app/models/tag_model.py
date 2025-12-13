from sqlalchemy import Column, String, Integer, UniqueConstraint, Index

from app.models.base_model import BaseModel


class Tag(BaseModel):
    """标签模型"""
    
    __tablename__ = "tags"
    
    name = Column(String(50), nullable=False, comment="标签名称")
    status = Column(Integer, nullable=False, default=1, comment="状态：0-禁用，1-启用")
    color = Column(String(20), default="#3B82F6", nullable=False, comment="颜色标记")
    delete_flag = Column(Integer, nullable=False, default=0, comment="删除标志：0-未删除，1-已删除")
    
    __table_args__ = (
        UniqueConstraint("name", "delete_flag", name="uq_tags_name_delete_flag", comment="标签名称唯一索引（考虑删除状态）"),
        Index("idx_tags_status", "status"),
        Index("idx_tags_delete_flag", "delete_flag"),
        Index("idx_tags_color", "color"),
        Index("idx_tags_create_time", "create_time"),
        Index("idx_tags_update_time", "update_time"),
    )

