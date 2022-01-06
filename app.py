import logging

from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from core.config import settings
from handlers.v1.bot import register_bot
from middlewares.db_middleware import DbMiddleware

bot = Bot(token=settings.bot.token)
bot_dp = Dispatcher(bot)


async def on_startup(dp: Dispatcher):
    await bot.set_webhook(settings.bot.webhook_url)


async def on_shutdown(dp: Dispatcher):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bot stopped!')


def start():
    bot_dp.middleware.setup(LoggingMiddleware())
    bot_dp.middleware.setup(DbMiddleware())
    register_bot(bot_object=bot, dp=bot_dp)

    if settings.debug:
        executor.start_polling(bot_dp, skip_updates=True)
    else:
        start_webhook(
            dispatcher=bot_dp,
            webhook_path=settings.bot.webhook_url,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host='0.0.0.0',
            port=settings.port,
        )


if __name__ == '__main__':
    start()
