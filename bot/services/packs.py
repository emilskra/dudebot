from typing import List

from models.models import Pack


def get_packs() -> List[Pack]:
    return Pack.all()


def get_pack(pack_id: int) -> Pack:
    return Pack.get(id=pack_id)
