#! /usr/bin/env python3
import logging
import asyncio

from sqlalchemy import delete

from db.session import async_session
from models.questions_models import Question, Pack
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PACKS = (
    {
        "id": 1,
        "name": "Yura",
        "intro": "AwACAgIAAxkDAAIHxGGZcgRl3eYJYROt1rvVOqNpK5HcAAIPFgACJEbISMhgq5joEco-IgQ",
    },
    {
        "id": 2,
        "name": "Misc",
        "intro": "AwACAgIAAxkDAAIHxGGZcgRl3eYJYROt1rvVOqNpK5HcAAIPFgACJEbISMhgq5joEco-IgQ",
        "outro": "AwACAgIAAxkDAAIHxWGZcgW86hp0pcs_YyvNWyAdlEkVAAIQFgACJEbISG1MVs8o4-AGIgQ",
    },
)

QUESTIONS = (
    {
        "id": 1,
        "pack": 1,
        "file_id": "AwACAgIAAxkDAAIHwWGZcgS16OrbJRJ-Swtt60VRluvLAAIMFgACJEbISKI0qwOZbMnvIgQ",
        "order": 1,
    },
    {
        "id": 2,
        "pack": 1,
        "file_id": "AwACAgIAAxkDAAIHwmGZcgTEJtDVIFWNpRh7UfCmBaxGAAINFgACJEbISJ53LllDNJT7IgQ",
        "order": 2,
    },
    {
        "id": 3,
        "pack": 2,
        "file_id": "AwACAgIAAxkDAAIHw2GZcgSRQJ33JOx65JcGDXlBi6cTAAIOFgACJEbISA0RQ6LlUCmBIgQ",
        "order": 1,
    },
)


async def db_add(model, objs: tuple):
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
    await db_add(Pack, PACKS)
    await db_add(Question, QUESTIONS)


async def async_main() -> None:
    logger.info("Cleaning old data")
    await clean_db()
    logger.info("Creating initial data")
    await init_db()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(async_main())
