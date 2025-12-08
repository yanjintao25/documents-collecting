from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions import TagNotFoundError, TagAlreadyExistsError
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagCreate, TagUpdate, TagResponse


class TagService:
    """标签服务类"""
    
    def __init__(self, db: Session):
        self.repository = TagRepository(db)
        self.db = db
    
    def create_tag(self, tag_data: TagCreate) -> TagResponse:
        """创建标签"""
        # 检查标签是否已存在
        existing_tag = self.repository.get_by_name(tag_data.name)
        if existing_tag:
            raise TagAlreadyExistsError(tag_data.name)
        
        tag = self.repository.create(tag_data)
        return TagResponse.model_validate(tag)
    
    def get_tag(self, tag_id: int) -> TagResponse:
        """获取标签"""
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(tag_id)
        return TagResponse.model_validate(tag)
    
    def get_all_tags(self) -> List[TagResponse]:
        """获取所有标签"""
        tags = self.repository.get_all()
        return [TagResponse.model_validate(tag) for tag in tags]
    
    def update_tag(
        self,
        tag_id: int,
        update_data: TagUpdate,
    ) -> TagResponse:
        """更新标签"""
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(tag_id)
        
        # 检查名称是否与其他标签冲突
        if update_data.name != tag.name:
            existing_tag = self.repository.get_by_name(update_data.name)
            if existing_tag:
                raise TagAlreadyExistsError(update_data.name)
        
        updated_tag = self.repository.update(tag, update_data)
        return TagResponse.model_validate(updated_tag)
    
    def delete_tag(self, tag_id: int) -> None:
        """删除标签"""
        tag = self.repository.get_by_id(tag_id)
        if not tag:
            raise TagNotFoundError(tag_id)
        
        self.repository.delete(tag)

