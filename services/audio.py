from typing import Optional

from pydub import AudioSegment

from services.exceptions import AudioFileGenerationError
from services.storages.base_storage import AbstractStorage
from services.storages.storage import get_storage


class Audio:

    def __init__(
            self,
            storage: AbstractStorage,
    ):
        self.storage = storage

    async def get_finish_file(self, file_ids: list[str]) -> Optional[str]:

        saved_files = await self.storage.save_files(file_ids)
        if len(saved_files) == 0:
            return

        file = AudioSegment.empty()
        for voice_file in saved_files:
            file += AudioSegment.from_ogg(voice_file)

        file_name = f"finish_files/.ogg"
        exported_file = file.export(file_name, bitrate="192k")
        if not exported_file:
            raise AudioFileGenerationError

        return exported_file

    async def clear(self, file_ids: list[str]) -> None:
        await self.storage.delete_files(file_ids)


def get_audio() -> Audio:
    storage = get_storage()
    return Audio(
        storage=storage,
    )
