from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.config.config import settings


class Base(DeclarativeBase):
    pass



engine = create_async_engine(settings.database.url)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """
    Yields a fresh SQLAlchemy AsynsSession.
    """
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with session_factory() as session:
        yield session