from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db, async_session
from models.questions_models import Pack, Question


class PackRepo(object):


    async def get(self, pack_id: int) -> Pack:
        async with async_session.begin() as session:
            pack = await session.get(Pack, pack_id)
            return pack

    async def get_packs(self) -> list[Pack]:
        async with async_session.begin() as session:
            packs = await session.execute(
                select(
                    Pack.id,
                    Pack.name,
                ),
            )

            return packs.all()

    async def get_question(self, pack_id: int, question_number: int) -> Question:
        async with async_session.begin() as session:
            question = await session.execute(
                select(
                    Question.id,
                    Question.file_id,
                    Question.order,
                ).where(
                    Question.pack == pack_id,
                    Question.order == question_number,
                )
            )

            return question.first()


async def get_pack_repo():
    return PackRepo()
