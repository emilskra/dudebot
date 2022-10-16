import os.path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class BotSettings(BaseSettings):
    token: Optional[str] = "1502829486:AAHr60kaoCuoh5880Y9chqsx4Vr6ZrZWiQs"
    webhook_host: str = Field('localhost', env='URL')
    webhook_path: Optional[str] = None
    webhook_url: Optional[str] = None

    @validator("webhook_path", pre=True, always=True)
    def set_webhook_path(cls, v: Optional[str], values) -> str:  # noqa
        return f'/webhook/{values.get("token")}'

    @validator("webhook_url", pre=True, always=True)
    def set_webhook_url(cls, v: Optional[str], values) -> str:  # noqa
        return f'{values.get("webhook_host")}{values.get("webhook_path")}'


class YDBSettings(BaseSettings):
    database_host: str = Field('grpc://localhost:2136')
    database_name: str = Field('/local')


class ProjectSettings(BaseSettings):
    project_name: str = 'Dude Bot'
    base_dir: str = os.path.dirname(os.path.dirname(__file__))
    debug: bool = Field(False, env='BOT_DEBUG')
    test: bool = Field(False, env="BOT_TEST")
    port: int = Field(9000)
    lambda_concat_url: str = Field('https://functions.yandexcloud.net/d4e7lv30afsp1onahojv')

    database: YDBSettings = YDBSettings()
    bot: BotSettings = BotSettings()

    class Config:
        env_file = '.env'


settings = ProjectSettings()
