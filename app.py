import logging

from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram import Bot
from aiogram.dispatcher import Dispatcher

from src.core.config import settings
from src.handlers.v1.bot import register_bot
from src.db.db_middleware import DbMiddleware

bot = Bot(token=settings.bot.token)
bot_dp = Dispatcher(bot)


async def on_startup(dp: Dispatcher):
    ...


async def on_shutdown(dp: Dispatcher):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bot stopped!')


def main():
    bot_dp.middleware.setup(LoggingMiddleware())
    bot_dp.middleware.setup(DbMiddleware())
    register_bot(bot_object=bot, dp=bot_dp)
    logging.error(settings)
    if settings.debug:
        executor.start_polling(bot_dp, skip_updates=True)
    else:
        logging.warning("Webhook")
        start_webhook(
            dispatcher=bot_dp,
            webhook_path=settings.bot.webhook_path,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host='0.0.0.0',
            port=settings.port,
        )


if __name__ == '__main__':
    start()
