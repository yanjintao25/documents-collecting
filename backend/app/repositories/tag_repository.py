from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.tag_model import Tag
from app.schemas.tag import TagCreate, TagUpdate


class TagRepository:
    """标签仓库类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, tag_data: TagCreate) -> Tag:
        """创建标签"""
        tag = Tag(**tag_data.model_dump())
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def get_by_id(self, tag_id: int) -> Optional[Tag]:
        """通过ID获取标签"""
        return self.db.query(Tag).filter(Tag.id == tag_id).first()
    
    def get_by_name(self, name: str) -> Optional[Tag]:
        """通过名称获取标签"""
        return self.db.query(Tag).filter(Tag.name == name).first()
    
    def get_all(self) -> List[Tag]:
        """获取所有标签"""
        return self.db.query(Tag).all()
    
    def update(self, tag: Tag, update_data: TagUpdate) -> Tag:
        """更新标签"""
        tag.name = update_data.name
        tag.color = update_data.color
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def delete(self, tag: Tag) -> None:
        """删除标签"""
        self.db.delete(tag)
        self.db.commit()

