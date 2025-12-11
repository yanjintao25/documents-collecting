from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class BaseModel(Base):
    """基础模型类"""
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, comment="创建时间")
    update_time = Column(DateTime(timezone=True), onupdate=func.now(), nullable=False, comment="更新时间")

