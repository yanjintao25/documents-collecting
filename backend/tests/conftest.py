"""
测试配置和共享 fixtures
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app.core.dependencies import get_database
from app.core.config import settings
from app.main import app


# 创建临时数据库
@pytest.fixture(scope="session")
def test_db():
    """创建测试数据库"""
    # 使用内存数据库进行测试
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # 清理
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(test_db):
    """创建数据库会话"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session):
    """创建测试客户端"""
    def override_get_database():
        try:
            yield db_session
        finally:
            pass
    
    # 覆盖依赖注入
    app.dependency_overrides[get_database] = override_get_database
    
    with TestClient(app) as test_client:
        yield test_client
    
    # 清理覆盖
    app.dependency_overrides.clear()


@pytest.fixture
def temp_upload_dir(monkeypatch):
    """创建临时上传目录"""
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)
    
    # 使用 monkeypatch 临时修改配置
    original_upload_dir = settings.UPLOAD_DIR
    monkeypatch.setattr(settings, "UPLOAD_DIR", temp_dir)
    
    # 确保目录存在
    temp_path.mkdir(parents=True, exist_ok=True)
    
    yield temp_path
    
    # 清理
    shutil.rmtree(temp_dir, ignore_errors=True)
    monkeypatch.setattr(settings, "UPLOAD_DIR", original_upload_dir)


@pytest.fixture
def sample_pdf_file():
    """创建示例PDF文件内容"""
    # 这是一个最小的有效PDF文件
    pdf_content = b"""%PDF-1.4
1 0 obj
<<
/Type /Catalog
/Pages 2 0 R
>>
endobj
2 0 obj
<<
/Type /Pages
/Kids [3 0 R]
/Count 1
>>
endobj
3 0 obj
<<
/Type /Page
/Parent 2 0 R
/MediaBox [0 0 612 792]
/Contents 4 0 R
/Resources <<
/Font <<
/F1 <<
/Type /Font
/Subtype /Type1
/BaseFont /Helvetica
>>
>>
>>
>>
endobj
4 0 obj
<<
/Length 44
>>
stream
BT
/F1 12 Tf
100 700 Td
(Test PDF) Tj
ET
endstream
endobj
xref
0 5
0000000000 65535 f
0000000009 00000 n
0000000058 00000 n
0000000115 00000 n
0000000306 00000 n
trailer
<<
/Size 5
/Root 1 0 R
>>
startxref
400
%%EOF"""
    return pdf_content


@pytest.fixture
def sample_text_file():
    """创建示例文本文件内容"""
    return b"This is a test text file content."


@pytest.fixture
def sample_tag(db_session):
    """创建示例标签"""
    from app.models.tag_model import Tag
    
    tag = Tag(name="测试标签", color="#FF0000")
    db_session.add(tag)
    db_session.commit()
    db_session.refresh(tag)
    
    return tag
