import abc
import io
from http import HTTPStatus

import aiohttp
from pydantic import BaseModel

from src.core.config import settings
from src.services.exceptions import AudioJoinError


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
                    settings.lambda_concat_url,
                    json=data.dict(),
                    ssl=False
            ) as response:
                if response.status != HTTPStatus.OK:
                    raise AudioJoinError(await response.json())

                return io.BytesIO(await response.read())


def get_audio() -> BaseAudio:
    return AudioLambda()
