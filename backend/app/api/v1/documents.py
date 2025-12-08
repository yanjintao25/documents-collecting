from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.dependencies import get_database
from app.services.document_service import DocumentService
from app.schemas.document import DocumentResponse, DocumentUpdate

router = APIRouter(prefix="/documents", tags=["文档管理"])


@router.post("/upload", response_model=DocumentResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tag_ids: Optional[str] = Form(None),  # 接收逗号分隔的标签ID字符串
    db: Session = Depends(get_database),
):
    """
    上传文档
    
    - **file**: 上传的文件
    - **description**: 文档描述（可选）
    - **tag_ids**: 标签ID，逗号分隔（可选）
    """
    service = DocumentService(db)
    
    # 解析标签ID
    tag_id_list = None
    if tag_ids:
        tag_id_list = [int(tid) for tid in tag_ids.split(",") if tid.strip()]
    
    return service.upload_document(
        file=file,
        description=description,
        tag_ids=tag_id_list,
    )


@router.get("/", response_model=List[DocumentResponse])
def get_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database),
):
    """
    获取文档列表
    
    - **skip**: 跳过的记录数
    - **limit**: 返回的记录数限制
    """
    service = DocumentService(db)
    return service.get_documents(skip=skip, limit=limit)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_database),
):
    """获取单个文档信息"""
    service = DocumentService(db)
    return service.get_document(document_id)


@router.get("/{document_id}/download")
def download_document(
    document_id: int,
    db: Session = Depends(get_database),
):
    """下载文档"""
    service = DocumentService(db)
    file_path = service.get_file_path(document_id)
    
    # 获取原始文件名
    document = service.get_document(document_id)
    
    return FileResponse(
        path=str(file_path),
        filename=document.original_filename,
        media_type=document.file_type,
    )


@router.put("/{document_id}", response_model=DocumentResponse)
def update_document(
    document_id: int,
    update_data: DocumentUpdate,
    db: Session = Depends(get_database),
):
    """更新文档信息"""
    service = DocumentService(db)
    return service.update_document(document_id, update_data)


@router.delete("/{document_id}", status_code=204)
def delete_document(
    document_id: int,
    db: Session = Depends(get_database),
):
    """删除文档"""
    service = DocumentService(db)
    service.delete_document(document_id)
    return None

