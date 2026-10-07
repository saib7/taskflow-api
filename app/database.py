from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Every ORM model in app/models.py inherits from this."""


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    # everything before `yield` runs on the way in, everything after
    # runs on the way out -- even if the endpoint raises an exception
    async with AsyncSessionLocal() as session:
        yield session