from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from db.session import get_session, close_session


class DbMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    async def pre_process(self, obj, data, *args):
        data["db"] = await get_session()

    async def post_process(self, obj, data, *args):
        db = data.get("db")
        if db:
            await close_session(db)
