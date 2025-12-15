from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_database
from app.services.category_service import CategoryService
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["分类管理"])


@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_database),
):
    """创建分类"""
    service = CategoryService(db)
    return service.create_category(category)


@router.get("/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_database)):
    """获取所有分类"""
    service = CategoryService(db)
    return service.get_all_categories()


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_database),
):
    """获取单个分类"""
    service = CategoryService(db)
    return service.get_category(category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_database),
):
    """更新分类"""
    service = CategoryService(db)
    return service.update_category(category_id, category)


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    db: Session = Depends(get_database),
):
    """删除分类"""
    service = CategoryService(db)
    service.delete_category(category_id)
    return None
