from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_database
from app.services.tag_service import TagService
from app.schemas.tag import TagCreate, TagUpdate, TagResponse

router = APIRouter(prefix="/tags", tags=["标签管理"])


@router.post("/", response_model=TagResponse, status_code=201)
def create_tag(
    tag: TagCreate,
    db: Session = Depends(get_database),
):
    """创建标签"""
    service = TagService(db)
    return service.create_tag(tag)


@router.get("/", response_model=List[TagResponse])
def get_tags(db: Session = Depends(get_database)):
    """获取所有标签"""
    service = TagService(db)
    return service.get_all_tags()


@router.get("/{tag_id}", response_model=TagResponse)
def get_tag(
    tag_id: int,
    db: Session = Depends(get_database),
):
    """获取单个标签"""
    service = TagService(db)
    return service.get_tag(tag_id)


@router.put("/{tag_id}", response_model=TagResponse)
def update_tag(
    tag_id: int,
    tag: TagUpdate,
    db: Session = Depends(get_database),
):
    """更新标签"""
    service = TagService(db)
    return service.update_tag(tag_id, tag)


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
    tag_id: int,
    db: Session = Depends(get_database),
):
    """删除标签"""
    service = TagService(db)
    service.delete_tag(tag_id)
    return None

