from unittest.mock import AsyncMock

import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from models.base import Base
from repositories.interview_repo import InterviewRepo
from repositories.pack_repo import PackRepo
from repositories.question_repo import QuestionRepo
from services.base import register_services
from services.interview import InterviewService, InterviewFinishService
from services.pack import PackService
from core.config import settings


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    engine = create_async_engine(
        f"{settings.database.database_host}/bot_test", poolclass=NullPool
    )

    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        yield engine
    finally:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        await engine.dispose()


@pytest.fixture(scope="function", autouse=True)
async def clean_db(test_db):
    yield

    async with test_db.begin() as con:
        for table in reversed(Base.metadata.sorted_tables):
            await con.execute(table.delete())


@pytest.fixture(scope="session")
async def pack_repo(test_db) -> PackRepo:
    return PackRepo(test_db)


@pytest.fixture(scope="session")
async def pack_service(pack_repo: PackRepo):
    return PackService(pack_repo)


@pytest.fixture(scope="session")
async def interview_repo(test_db) -> InterviewRepo:
    return InterviewRepo(test_db)


@pytest.fixture(scope="session")
async def question_repo(test_db) -> QuestionRepo:
    return QuestionRepo(test_db)


@pytest.fixture(scope="session")
def interview_service(
    interview_repo: InterviewRepo, question_repo: QuestionRepo
) -> InterviewService:
    return InterviewService(interview_repo, question_repo)


@pytest.fixture(scope="session")
def interview_finish_service(
    interview_service: InterviewService, pack_service: PackService
) -> InterviewFinishService:
    return InterviewFinishService(interview_service, pack_service, AsyncMock())


@pytest.fixture(scope="session")
def bot(test_db) -> AsyncMock:
    register_services(test_db)
    return AsyncMock()
