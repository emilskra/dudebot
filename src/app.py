import logging

from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from db.session import init_engine, close_session_pool
from setup import register_handlers, register_middlewares
from core.config import settings
from services.base import register_services

bot = Bot(token=settings.bot.token)
bot_dp = Dispatcher(bot)


async def on_startup(dp: Dispatcher):
    engine = await init_engine()
    register_services(engine)


async def on_shutdown(dp: Dispatcher):
    logging.warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()

    await close_session_pool()
    logging.warning("Bot stopped!")


def main():

    register_handlers(bot_dp)
    register_middlewares(bot, bot_dp)
    if settings.debug:
        executor.start_polling(
            bot_dp,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
        )
    else:
        logging.warning("Webhook")
        start_webhook(
            dispatcher=bot_dp,
            webhook_path=settings.bot.webhook_path,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host="0.0.0.0",
            port=settings.port,
        )


if __name__ == "__main__":
    main()
