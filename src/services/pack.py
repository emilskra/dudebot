from repositories.pack_repo import PackRepo
from schemas.pack_schema import Pack, PackGet
from services.exceptions import PackNotFound


class PackService:
    def __init__(self, pack_repo: PackRepo):
        self.pack_repo = pack_repo

    async def get_pack(self, pack_id: int) -> Pack:
        pack = await self.pack_repo.get_pack(pack_id)
        if not pack:
            raise PackNotFound
        return Pack.from_orm(pack)

    async def get_all(self) -> list[PackGet]:
        packs_db = await self.pack_repo.get_all_packs()
        return [PackGet(**pack) for pack in packs_db]
