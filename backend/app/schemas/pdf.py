from pydantic import BaseModel, Field
from typing import List, Optional


class PDFGenerateRequest(BaseModel):
    """PDF 生成请求模式"""
    
    document_ids: List[int] = Field(..., description="文档ID列表", min_items=1)
    title: Optional[str] = Field(default="文档汇编", description="PDF 标题")

