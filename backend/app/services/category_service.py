from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions import CategoryNotFoundError, CategoryAlreadyExistsError
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse


class CategoryService:
    """分类服务类"""
    
    def __init__(self, db: Session):
        self.repository = CategoryRepository(db)
        self.db = db
    
    def create_category(self, category_data: CategoryCreate) -> CategoryResponse:
        """创建分类"""
        # 检查分类是否已存在
        existing_category = self.repository.get_by_name(category_data.name)
        if existing_category:
            raise CategoryAlreadyExistsError(category_data.name)
        
        category = self.repository.create(category_data)
        return CategoryResponse.model_validate(category)
    
    def get_category(self, category_id: int) -> CategoryResponse:
        """获取分类"""
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        return CategoryResponse.model_validate(category)
    
    def get_all_categories(self) -> List[CategoryResponse]:
        """获取所有分类"""
        categories = self.repository.get_all()
        return [CategoryResponse.model_validate(category) for category in categories]
    
    def update_category(
        self,
        category_id: int,
        update_data: CategoryUpdate,
    ) -> CategoryResponse:
        """更新分类"""
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        
        # 检查名称是否与其他分类冲突
        if update_data.name != category.name:
            existing_category = self.repository.get_by_name(update_data.name)
            if existing_category:
                raise CategoryAlreadyExistsError(update_data.name)
        
        updated_category = self.repository.update(category, update_data)
        return CategoryResponse.model_validate(updated_category)
    
    def delete_category(self, category_id: int) -> None:
        """删除分类"""
        category = self.repository.get_by_id(category_id)
        if not category:
            raise CategoryNotFoundError(category_id)
        
        self.repository.delete(category)
