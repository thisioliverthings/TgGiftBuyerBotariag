from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    pass


async_engine: AsyncEngine = create_async_engine(url=settings.database_url)

AsyncSessionLocal: AsyncSession = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, autoflush=False
)
