#! /usr/bin/env python3
import json
import logging
import asyncio
import os

from sqlalchemy import delete

from db.session import async_session
from models.questions_models import Question, Pack
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PACKS_DATA = os.getenv('PACKS_DATA', 'dev')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', PACKS_DATA)


async def db_add(model, objs: list):
    async with async_session() as session:
        for obj in objs:
            db_obj = model(**obj)
            session.add(db_obj)
        await session.commit()


async def clean_db():
    async with async_session() as session:
        for table in (Pack, Question):
            await session.execute(delete(table))
        await session.commit()


async def init_db():
    packs_file = os.path.join(DATA_DIR, "packs.json")
    questions_file = os.path.join(DATA_DIR, "questions.json")

    with open(packs_file, 'r') as f:
        data: list = json.load(f)
        await db_add(Pack, data)

    with open(questions_file, 'r') as f:
        data: list = json.load(f)
        await db_add(Question, data)


async def async_main() -> None:
    logger.info("Cleaning old data")
    await clean_db()
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(async_main())
