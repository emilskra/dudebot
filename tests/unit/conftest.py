import asyncio
import json
import os
import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from .settings import settings


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def init_test_data(db: AsyncSession):

    statement = text(
        """
        TRUNCATE TABLE packs CASCADE;
    """)
    await db.execute(statement)

    statement = text(
        """
        TRUNCATE TABLE questions CASCADE;
    """)
    await db.execute(statement)
    await db.commit()

    packs_file = os.path.join(settings.data_dir, "packs.json")
    questions_file = os.path.join(settings.data_dir, "questions.json")
    with open(packs_file, 'r') as f:
        data = json.load(f)

        statement = text("""
            INSERT INTO packs(id, name, intro, outro) 
            VALUES(:id, :name, :intro, :outro)
        """)
        for pack in data:
            await db.execute(statement, pack)

    with open(questions_file, 'r') as f:
        data = json.load(f)

        statement = text("""
            INSERT INTO questions(id, pack, file_id, sort_order) 
            VALUES(:id, :pack, :file_id, :sort_order)
        """)
        for question in data:
            await db.execute(statement, question)

    await db.commit()


@pytest.fixture
async def db():
    engine = create_async_engine(settings.database.sqlalchemy_uri)
    async_session = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    session = async_session()
    await session.begin()
    yield session
    await session.rollback()
    await session.close()

