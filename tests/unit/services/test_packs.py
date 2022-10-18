from models.pack_model import PackModel
from repositories.pack_repo import PackRepo
from services.pack import PackService
from tests.unit.utils import db_inserts


async def test_get_packs(test_db, pack_service: PackService, pack_repo: PackRepo):
    packs_data = {PackModel: [{"id": 1, "name": "pack1"}, {"id": 2, "name": "pack2"}]}
    await db_inserts(test_db, packs_data)

    packs = await pack_service.get_all()

    assert len(packs) == 2


async def test_get_pack(test_db, pack_service: PackService, pack_repo: PackRepo):
    packs_data = {PackModel: {"id": 1, "name": "pack1"}}
    await db_inserts(test_db, packs_data)

    packs = await pack_service.get_pack(1)

    assert packs.id == 1
