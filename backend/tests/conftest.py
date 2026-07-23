import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from typing import AsyncGenerator

from app.core.database import Base
from app.core.config import get_settings
from app.models.experiment import Experiment
from app.models.persona import Persona
from app.models.survey import Survey
from app.models.response import Response
from app.models.interview import InterviewSession
from app.models.insight import Insight
from app.models.report import Report

settings = get_settings()

# Use MySQL (aiomysql) for all tests — same DB as the application.
# Tables are created fresh before each test and dropped afterwards.
test_engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
)

TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    """Create and drop tables for every test to ensure a clean state."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide a database session to the test."""
    async with TestSessionLocal() as session:
        yield session
