import motor.motor_asyncio as motor_async

from src.schemas.pack_schema import Pack, Question
from src.schemas.base import PyObjectId


class PackRepo(object):

    def __init__(self, db: motor_async.AsyncIOMotorClient):
        self.db = db
        self.document = db["packs"]

    async def get(self, pack_id: PyObjectId) -> Pack:
        pack = await self.document.find_one({"_id": pack_id})
        return pack

    async def get_packs(self) -> list[Pack]:
        packs = await self.document.find()
        return packs

    async def get_question(self, pack_id: PyObjectId, question_number: int) -> Question:
        pack = await self.get(pack_id)
        return pack.questions[question_number]


async def get_pack_repo(db: motor_async.AsyncIOMotorClient):
    return PackRepo(db)
