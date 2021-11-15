from sqlalchemy import select
from sqlalchemy.orm import Session

from db.session import get_db
from models.questions_models import Pack, Question


class PackRepo(object):

    def __init__(self, db: Session):
        self.db = db

    async def get(self, pack_id: int) -> Pack:
        pass

    async def get_packs(self):
        pass

    async def get_pack_questions(self, pack_id: int):
        pass

    async def get_question(self, pack_id: int, question_number: int) -> Question:
        question = await self.db.execute(
            select(
                Question,
            ).where(
                Question.pack == pack_id,
                Question.order == question_number,
            )
        )

        return question


def get_pack_repo():
    db: Session = get_db()

    return PackRepo(
        db=db,
    )
