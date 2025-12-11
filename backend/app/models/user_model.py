from sqlalchemy import Column, String, Integer, Index

from app.models.base_model import BaseModel


class User(BaseModel):
    """用户模型"""
    
    __tablename__ = "users"
    
    username = Column(String(50), nullable=False, comment="用户名")
    password = Column(String(255), nullable=False, comment="密码（加密存储）")
    email = Column(String(100), nullable=False, comment="邮箱")
    phone = Column(String(20), nullable=True, comment="手机号")
    status = Column(Integer, nullable=False, default=1, comment="状态：0-禁用，1-正常，2-未激活")
    delete_flag = Column(Integer, nullable=False, default=0, comment="删除标志：0-未删除，1-已删除")
    
    __table_args__ = (
        Index("uk_users_phone", "phone", unique=True, comment="手机号唯一索引（忽略 NULL）"),
        Index("idx_users_status", "status", comment="状态索引"),
        Index("idx_users_delete_flag", "delete_flag", comment="删除标志索引"),
        Index("idx_users_create_time", "create_time", comment="创建时间索引"),
        Index("idx_users_update_time", "update_time", comment="更新时间索引"),
    )

