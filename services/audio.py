import os
from typing import Optional
from aiogram import Bot
from pydub import AudioSegment


class Audio:

    def __init__(self, bot: Bot, file_ids: list[str]):
        self.bot = bot
        self.file_ids = file_ids

    async def get_finish_file(self) -> Optional[str]:
        if not os.path.exists("finish_files/"):
            os.mkdir("finish_files/")

        files = []
        for file_id in self.file_ids:
            file_name = f"finish_files/{file_id}.ogg"

            if not os.path.exists(file_name):
                await bot.download_file_by_id(file_id, file_name)

            files.append(file_name)

        if len(files) == 0:
            return None

        file = AudioSegment.empty()
        for voice in files:
            file += AudioSegment.from_ogg(voice)

        file_name = f"finish_files/.ogg"
        return file.export(file_name, bitrate="192k")

    async def clear(self) -> None:
        for file_id in self.file_ids:
            os.remove(f"finish_files/{file_id}.ogg")


def get_audio(bot: Bot, file_ids: list[str]):
    return Audio(bot, file_ids)
