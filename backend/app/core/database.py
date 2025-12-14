from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool, NullPool
from typing import Generator

from app.core.config import settings

# 创建数据库引擎
# 对于 SQLite，使用 StaticPool 或 NullPool，因为 SQLite 不支持真正的连接池
is_sqlite = "sqlite" in settings.DATABASE_URL
connect_args = {}
poolclass = None

if is_sqlite:
    # SQLite 特定配置
    connect_args = {
        "check_same_thread": False,  # 允许多线程访问
        "timeout": 20,  # 连接超时时间（秒）
    }
    poolclass = StaticPool  # 使用静态连接池，适合 SQLite

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    poolclass=poolclass,
    echo=settings.DEBUG,  # 在 DEBUG 模式下打印 SQL 语句
    pool_pre_ping=True,  # 连接前检查连接是否有效（对非 SQLite 数据库有用）
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()


def get_db() -> Generator:
    """
    获取数据库会话
    
    Yields:
        Session: 数据库会话对象
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """初始化数据库，创建所有表"""
    Base.metadata.create_all(bind=engine)

