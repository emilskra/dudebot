from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

from models.pack_model import PackModel
from schemas.pack_schema import Pack


class PackRepo:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def get_pack(self, pack_id: int) -> Pack:
        async with self.engine.begin() as session:
            packs = await session.execute(
                select(PackModel).where(PackModel.id == pack_id)
            )
            return packs.fetchone()

    async def get_all_packs(self) -> list[dict]:
        async with self.engine.begin() as session:
            packs = await session.execute(select(PackModel.id, PackModel.name))
            return packs.fetchall()

    async def get_user_pack(self, user_id: int):
        ...
