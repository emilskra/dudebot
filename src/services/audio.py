import abc
import io
import os
from http import HTTPStatus
from typing import Union

import aiohttp
from aiogram import Bot
from pydantic import BaseModel
from pydub import AudioSegment

from core.config import settings
from services.exceptions import AudioJoinError


class ConcatFiles(BaseModel):
    files: list[str]
    finishFilename: str


class BaseAudio(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    async def join_files(file_ids: list[str], joined_file_name: str) -> io.BytesIO:
        ...


class AudioLambda(BaseAudio):
    @staticmethod
    async def join_files(file_ids: list[str], joined_file_name: str) -> io.BytesIO:

        async with aiohttp.ClientSession() as session:
            data = ConcatFiles(
                files=file_ids,
                finishFilename=joined_file_name,
            )
            async with session.post(
                settings.lambda_concat_url, json=data.dict(), ssl=False
            ) as response:
                if response.status != HTTPStatus.OK:
                    raise AudioJoinError(await response.json())

                return io.BytesIO(await response.read())


class AudioFfmpeg(BaseAudio):

    def __init__(self, bot: Bot):
        self.bot = bot

    async def save_files(self, file_sources: list[str]) -> list[str]:
        saved_files = []
        for source in file_sources:
            destination = os.path.join('/tmp', f'{source}.ogg')
            if not os.path.exists(destination):
                await self.bot.download_file_by_id(source, destination)

            saved_files.append(destination)

        return saved_files

    async def join_files(self, file_ids: list[str], joined_file_name: str) -> io.BufferedRandom:
        saved_files = await self.save_files(file_ids)
        if len(saved_files) == 0:
            raise AudioJoinError

        file = AudioSegment.empty()
        for voice_file in saved_files:
            file += AudioSegment.from_ogg(voice_file, parameters=["-acodec", "libopus"])

        export_file_path = os.path.join('/tmp', joined_file_name)
        exported_file = file.export(
            export_file_path,
            format="ogg",
            codec="libopus",
        )

        self.clear_files(saved_files)
        return exported_file

    @staticmethod
    def clear_files(file: Union[str, list[str]]):

        if isinstance(file, list):
            for file_name in file:
                os.remove(file_name)

            return

        os.remove(file)
