import os
from typing import Optional

from pydub import AudioSegment
from aiogram import Bot

from services.exceptions import AudioFileGenerationError
from core.config import settings


class Audio:

    @staticmethod
    async def get_finish_file(file_ids: list[str]) -> Optional[str]:
        bot = Bot(settings.bot.token)

        if not os.path.exists("finish_files/"):
            os.mkdir("finish_files/")

        files = []
        for file_id in file_ids:
            file_name = f"finish_files/{file_id}.ogg"

            if not os.path.exists(file_name):
                await bot.download_file_by_id(file_id, file_name)

            files.append(file_name)

        if len(files) == 0:
            return

        file = AudioSegment.empty()
        for voice in files:
            file += AudioSegment.from_ogg(voice)

        file_name = f"finish_files/.ogg"
        exported_file = file.export(file_name, bitrate="192k")
        if not exported_file:
            raise AudioFileGenerationError

        return exported_file

    @staticmethod
    async def clear(file_ids: list[str]) -> None:
        finish_files_dir = os.path.join(settings.base_dir, 'finish_files')
        for file_id in file_ids:
            file_path = os.path.join(finish_files_dir, f'{file_id}.ogg')

            if not os.path.exists(file_path):
                continue

            os.remove(file_path)


def get_audio() -> Audio:
    return Audio()
