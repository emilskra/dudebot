import logging
from typing import Optional
import ydb

from core.config import settings
SESSION_POOL: Optional[ydb.aio.SessionPool] = None


async def get_session_pool() -> ydb.aio.SessionPool:
    if SESSION_POOL is not None:
        return SESSION_POOL

    raise Exception("Session has not been initialized")


async def init_session_pool():

    driver = ydb.aio.Driver(
        endpoint='grpc://localhost:2136',
        database='/local'
    )
    logging.info("connecting to the database")
    await driver.wait(fail_fast=True)

    session_pool = ydb.aio.SessionPool(driver, size=10)

    global SESSION_POOL
    SESSION_POOL = session_pool


async def close_session_pool():
    if SESSION_POOL is not None:
        await SESSION_POOL.stop()

    raise Exception("Session has not been initialized")
