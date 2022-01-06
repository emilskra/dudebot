from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine = create_async_engine(settings.database_url)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            return session


async def close_session(session):
    await session.commit()
    await session.close()


@asynccontextmanager
async def get_db() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            try:
                yield session
                await session.commit()
            finally:
                await session.close()
