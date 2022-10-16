from repositories.pack_repo import PackRepo
from schemas.pack_schema import Pack


class PackService:

    def __init__(self, pack_repo: PackRepo):
        self.pack_repo = pack_repo

    async def get_pack(self, pack_id: int):
        return await self.pack_repo.get_pack(pack_id)

    async def get_all(self) -> list[Pack]:
        packs_db = await self.pack_repo.get_all_packs()
        return [Pack(**pack) for pack in packs_db]

    async def get_user_pack(self, user_id: int) -> Pack:
        return await self.pack_repo.get_user_pack(user_id)
