import os.path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class BotSettings(BaseSettings):
    token: str = Field(True, env='TOKEN')
    url = Field('localhost', env='URL')
    webhook_url: Optional[str] = None

    @validator("webhook_url", pre=True, always=False)
    def set_webhook_url(cls, v: Optional[str], values) -> str:  # noqa
        return f'/{values.get("url")}/{values.get("token")}'


class ProjectSettings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(__file__))
    project_name: str = 'Dude Bot'
    debug: bool = Field(False, env='BOT_DEBUG')
    test: bool = Field(False, env="BOT_TEST")
    port = Field(9000, env='PORT')
    bot: BotSettings = BotSettings()
    lambda_concat_url: str = Field('https://functions.yandexcloud.net/d4e7lv30afsp1onahojv', env='LAMBDA_CONCAT_URL')
    database_url: str = Field('', env='BOT_DATABASE_URL')


settings = ProjectSettings()
