from typing import List

from models.models import Pack, Question


def get_packs() -> List[Pack]:
    return Pack.all()


def get_pack(pack_id: int) -> Pack:
    return Pack.get(id=pack_id)


def get_pack_questions(pack_id: int) -> List[Question]:
    return Pack.questions.filter(pack=pack_id)
