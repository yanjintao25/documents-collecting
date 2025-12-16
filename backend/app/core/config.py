from pydantic_settings import BaseSettings
from typing import List, Optional
import os
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""
    
    # 应用信息
    APP_NAME: str = "文档管理系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 文件存储配置
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    
    # 数据库配置
    @property
    def DATABASE_URL(self) -> str:
        """获取数据库URL"""
        db_path = self.BASE_DIR / "database" / "sqlite" / "documents_collecting.db"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{db_path.as_posix()}"
    UPLOAD_DIR: str = "uploads"
    PDF_OUTPUT_DIR: str = "generated_pdfs"
    MAX_UPLOAD_SIZE: int = 104857600  # 100MB
    
    # LibreOffice 配置
    LIBREOFFICE_PATH: Optional[str] = None  # LibreOffice 可执行文件路径（可选，如果为空则自动检测）
    
    # CORS 配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    @property
    def upload_dir_path(self) -> Path:
        """获取上传目录路径"""
        path = self.BASE_DIR / self.UPLOAD_DIR
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    @property
    def pdf_output_dir_path(self) -> Path:
        """获取 PDF 输出目录路径"""
        path = self.BASE_DIR / self.PDF_OUTPUT_DIR
        path.mkdir(parents=True, exist_ok=True)
        return path
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

