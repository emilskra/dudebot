from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine

from core.config import settings

ENGINE: Optional[AsyncEngine] = None


def create_engine() -> AsyncEngine:
    return create_async_engine(
        url=settings.database.database_uri,
        pool_size=settings.database.pg_pool_max_size,
        pool_recycle=settings.database.pg_pool_recycle,
        pool_pre_ping=settings.database.pg_pool_pre_ping,
        pool_timeout=settings.database.pg_pool_timeout,
        connect_args={
            "timeout": settings.database.pg_connect_timeout,
        },
        echo=settings.database.pg_echo_enabled,
    )


async def get_engine() -> AsyncEngine:
    if ENGINE is not None:
        return ENGINE

    raise Exception("Session has not been initialized")


async def init_engine():
    global ENGINE
    ENGINE = create_engine()


async def close_session_pool():
    if ENGINE is not None:
        await ENGINE.dispose()

    raise Exception("Session has not been initialized")
