import os.path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class BotSettings(BaseSettings):
    token: str = Field(True, env='TOKEN')
    webhook_host: str = Field('localhost', env='URL')
    webhook_path: Optional[str] = None
    webhook_url: Optional[str] = None

    @validator("webhook_path", pre=True, always=True)
    def set_webhook_path(cls, v: Optional[str], values) -> str:  # noqa
        return f'/webhook/{values.get("token")}'

    @validator("webhook_url", pre=True, always=True)
    def set_webhook_url(cls, v: Optional[str], values) -> str:  # noqa
        return f'{values.get("webhook_host")}{values.get("webhook_path")}'


class ProjectSettings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(__file__))
    project_name: str = 'Dude Bot'
    debug: bool = Field(False, env='BOT_DEBUG')
    test: bool = Field(False, env="BOT_TEST")
    port: int = Field(9000, env='PORT')
    bot: BotSettings = BotSettings()
    lambda_concat_url: str = Field('https://functions.yandexcloud.net/d4e7lv30afsp1onahojv', env='LAMBDA_CONCAT_URL')
    database_url: str = Field('', env='BOT_DATABASE_URL')


settings = ProjectSettings()
