import os
from typing import Optional
from requests import get
from pydub import AudioSegment


class Audio:

    @staticmethod
    async def get_finish_file(file_ids: list) -> Optional[str]:
        if not os.path.exists("finish_files/"):
            os.mkdir("finish_files/")

        files = []
        for file in file_ids:
            file_name = f"finish_files/{file}.ogg"
            if not os.path.exists(file_name):
                r = get(get_file_url(os.getenv("TOKEN"), file))
                open(file_name, "wb").write(r.content)

            files.append(file_name)

        if len(files) == 0:
            return None

        file = AudioSegment.empty()
        for voice in files:
            file += AudioSegment.from_ogg(voice)

        return file.export(file_name, bitrate="192k")

    @staticmethod
    async def clear(file_ids: list) -> None:
        for file_id in file_ids:
            os.remove(f"finish_files/{file_id}.ogg")


def get_audio():
    return Audio()
