from repositories.pack_repo import PackRepo
from schemas.pack_schema import Pack
from services.pack import PackService


async def test_get_packs(pack_service: PackService, pack_repo: PackRepo):
    packs_data = [
        Pack(id=1, name="pack1"),
        Pack(id=2, name="pack2"),
    ]
    await pack_repo.add_packs(packs_data)

    packs = await pack_service.get_all()

    assert len(packs) == 2
