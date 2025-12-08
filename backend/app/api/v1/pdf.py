from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.dependencies import get_database
from app.services.pdf_service import PDFService
from app.schemas.pdf import PDFGenerateRequest

router = APIRouter(prefix="/pdf", tags=["PDF生成"])


@router.post("/generate")
def generate_pdf(
    request: PDFGenerateRequest,
    db: Session = Depends(get_database),
):
    """
    生成文档汇编 PDF
    
    - **document_ids**: 文档ID列表
    - **title**: PDF 标题（可选）
    """
    service = PDFService(db)
    output_path = service.generate_pdf(
        document_ids=request.document_ids,
        title=request.title,
    )
    
    return FileResponse(
        path=str(output_path),
        filename=output_path.name,
        media_type="application/pdf",
    )

