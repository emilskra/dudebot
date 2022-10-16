import pytest
import asyncio
import ydb

from repositories.pack_repo import PackRepo
from services.pack import PackService
from core.config import settings


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def db_session():
    driver = ydb.aio.Driver(
        endpoint=settings.database.database_host,
        database=settings.database.database_name,
        credentials=ydb.AnonymousCredentials(),
    )
    await driver.wait(fail_fast=True)

    session_pool = ydb.aio.SessionPool(driver, size=10)
    yield session_pool
    await session_pool.stop()


@pytest.fixture(scope='function')
async def clean_db(db_session):
    yield

    tables = ['interview_answers', 'interviews', 'pack_questions', 'packs', 'users']

    async def execute(session):
        for table in tables:
            query = f"""
            DELETE FROM {table};
            """
            prepared_query = await session.prepare(query)
            await session.transaction().execute(
                prepared_query,
                commit_tx=True,
            )

    await db_session.session_pool.retry_operation(execute)


@pytest.fixture(scope='session')
async def pack_repo(db_session) -> PackRepo:
    return PackRepo(db_session)


@pytest.fixture(scope='session')
async def pack_service(db_session, pack_repo: PackRepo):
    return PackService(pack_repo)
