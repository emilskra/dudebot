import os
from typing import Optional

from aiogram import Bot
from services.storages.base_storage import AbstractStorage

BOT: Optional[Bot] = None


class TelegramStorage(AbstractStorage):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def download_file(self, file_source: str, destination: str):
        await self.bot.download_file_by_id(file_source, destination)

    async def save_files(self, file_sources: list[str]) -> list[str]:
        if not os.path.exists("finish_files/"):
            os.mkdir("finish_files/")

        saved_files = []
        for source in file_sources:
            destination = f"finish_files/{source}.ogg"

            if not os.path.exists(destination):
                await self.download_file(source, destination)

            saved_files.append(destination)

        return saved_files

    @staticmethod
    async def delete_files(file_sources: list[str]):
        finish_files_dir = 'finish_files/'
        for source in file_sources:
            file_path = os.path.join(finish_files_dir, f'{source}.ogg')

            if not os.path.exists(file_path):
                continue

            os.remove(file_path)


def get_telegram_storage() -> TelegramStorage:
    return TelegramStorage(
        bot=BOT
    )


def set_bot(bot: Bot):
    global BOT
    BOT = bot
