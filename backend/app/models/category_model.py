from sqlalchemy import Column, String, Integer, UniqueConstraint, Index

from app.models.base_model import BaseModel


class Category(BaseModel):
    """分类模型"""
    
    __tablename__ = "categories"
    
    name = Column(String(100), nullable=False, comment="分类名称")
    status = Column(Integer, nullable=False, default=1, comment="状态：0-禁用，1-启用")
    delete_flag = Column(Integer, nullable=False, default=0, comment="删除标志：0-未删除，1-已删除")
    
    __table_args__ = (
        UniqueConstraint("name", "delete_flag", name="uq_categories_name_delete_flag", comment="分类名称唯一索引（考虑删除状态）"),
        Index("idx_categories_status", "status", comment="状态索引"),
        Index("idx_categories_delete_flag", "delete_flag", comment="删除标志索引"),
        Index("idx_categories_create_time", "create_time", comment="创建时间索引"),
        Index("idx_categories_update_time", "update_time", comment="更新时间索引"),
    )

