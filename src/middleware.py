from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware


class BotMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def pre_process(self, obj, data, *args):
        data["bot"] = self.bot
