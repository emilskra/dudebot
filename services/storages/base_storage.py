import abc


class AbstractStorage(abc.ABC):

    @abc.abstractmethod
    async def download_file(self, file_source: str, destination: str) -> None:
        ...

    @abc.abstractmethod
    async def save_files(self, file_sources: list[str]) -> list[str]:
        ...

    @staticmethod
    @abc.abstractmethod
    async def delete_files(file_sources: list[str]) -> None:
        ...
