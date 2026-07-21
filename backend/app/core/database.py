"""
Async SQLAlchemy engine + session factory.
Uses MySQL with the aiomysql async driver (mysql+aiomysql).
"""
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a request-scoped DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Database initialization.
    
    Tables are created via SQL scripts (sql/schema.sql and sql/seed.sql).
    Run: python scripts/setup_database.py
    
    This function is kept for compatibility but no longer auto-creates tables.
    """
    # Tables are now managed via SQL scripts
    # Run: python scripts/setup_database.py to initialize the database
    pass
