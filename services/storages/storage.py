from services.storages.base_storage import AbstractStorage
from services.storages.telegram_storage import get_telegram_storage


def get_storage() -> AbstractStorage:
    return get_telegram_storage()
