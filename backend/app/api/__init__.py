from fastapi import APIRouter

from app.api.v1 import documents, tags, search, pdf

api_router = APIRouter()

api_router.include_router(documents.router, prefix="/api/v1")
api_router.include_router(tags.router, prefix="/api/v1")
api_router.include_router(search.router, prefix="/api/v1")
api_router.include_router(pdf.router, prefix="/api/v1")

