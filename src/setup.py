from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentType

from middleware import BotMiddleware
from handlers.v1.bot import send_welcome, text_messages, handle_voice, pack_choose


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, commands=["start"])
    dp.register_message_handler(text_messages, content_types=ContentType.TEXT)
    dp.register_message_handler(handle_voice, content_types=ContentType.VOICE)
    dp.register_callback_query_handler(pack_choose, regexp="packs_[0-9]")


def register_middlewares(bot, dp: Dispatcher):
    dp.middleware.setup(LoggingMiddleware())
    dp.middleware.setup(BotMiddleware(bot))
