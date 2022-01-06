from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import async_session
from models.questions_models import Pack, Question


class PackRepo(object):

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get(self, pack_id: int) -> Pack:
        pack = await self.db.get(Pack, pack_id)
        return pack

    @staticmethod
    async def get_packs() -> list[Pack]:
        async with async_session.begin() as session:
            packs = await session.execute(
                select(
                    Pack.id,
                    Pack.name,
                ),
            )

            return packs.all()

    async def get_question(self, pack_id: int, question_number: int) -> Question:
        question = await self.db.execute(
            select(
                Question.id,
                Question.file_id,
                Question.sort_order,
            ).where(
                Question.pack == pack_id,
                Question.sort_order == question_number,
            )
        )

        return question.first()


async def get_pack_repo(db: AsyncSession):
    return PackRepo(db)
