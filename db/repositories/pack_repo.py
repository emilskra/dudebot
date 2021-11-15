from sqlalchemy.orm import Session

from db.session import get_db
from models.questions_models import Pack


class PackRepo(object):

    def __init__(self, db: Session):
        self.db = db

    async def get(self, pack_id: int) -> Pack:
        pass

    async def get_packs(self):
        pass

    async def get_pack_questions(self, pack_id: int):
        pass


def get_pack_repo():
    db: Session = get_db()

    return PackRepo(
        db=db,
    )
