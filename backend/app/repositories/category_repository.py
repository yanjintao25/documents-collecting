from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.category_model import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    """分类仓库类"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, category_data: CategoryCreate) -> Category:
        """创建分类"""
        category = Category(**category_data.model_dump())
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_by_id(self, category_id: int) -> Optional[Category]:
        """通过ID获取分类"""
        return self.db.query(Category).filter(
            Category.id == category_id,
            Category.delete_flag == 0
        ).first()
    
    def get_by_name(self, name: str) -> Optional[Category]:
        """通过名称获取分类（仅查询未删除的）"""
        return self.db.query(Category).filter(
            Category.name == name,
            Category.delete_flag == 0
        ).first()
    
    def get_all(self) -> List[Category]:
        """获取所有分类（仅查询未删除的）"""
        return self.db.query(Category).filter(Category.delete_flag == 0).all()
    
    def update(self, category: Category, update_data: CategoryUpdate) -> Category:
        """更新分类"""
        category.name = update_data.name
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete(self, category: Category) -> None:
        """删除分类"""
        self.db.delete(category)
        self.db.commit()
