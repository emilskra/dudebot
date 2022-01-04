import os.path
from logging import config as logging_config
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator


class PostgresDsnWithAsync(PostgresDsn):
    """ hack """
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}


class DataBaseSettings(BaseSettings):
    host: str = Field("localhost", env="POSTGRES_HOST")
    port: str = Field('5432', env="POSTGRES_PORT")
    name: str = Field("postgres", env="POSTGRES_DB")
    user: str = Field("postgres", env="POSTGRES_USER")
    password: str = Field("password", env="POSTGRES_PASSWORD")

    sqlalchemy_uri: Optional[str] = None

    @validator("sqlalchemy_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:  # noqa
        if isinstance(v, str):
            return v

        return PostgresDsnWithAsync.build(
            scheme="postgresql+asyncpg",
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            port=values.get("port"),
            path=f"/{values.get('name') or ''}",
        )


class BotSettings(BaseSettings):
    token: str = Field(True, env='TOKEN')
    webhook_host = Field('localhost', env='WEBHOOK_HOST')
    webhook_path = Field('/', env='WEBHOOK_PATH')
    webhook_url: Optional[str] = None

    @validator("webhook_url", pre=True, always=False)
    def set_webhook_url(cls, v: Optional[str], values: Dict[str, Any]) -> str:  # noqa
        if isinstance(v, str):
            return v

        return f'{values.get("webhook_host")}/{values.get("webhook_path")}'


class ProjectSettings(BaseSettings):
    base_dir: str = os.path.dirname(os.path.dirname(__file__))
    project_name: str = 'Dude Bot'
    debug: bool = Field(True, env='BOT_DEBUG')
    test: bool = Field(False, env="BOT_TEST")
    port = Field(9000, env='BOT_PORT')
    database: DataBaseSettings = DataBaseSettings()
    bot: BotSettings = BotSettings()
    lambda_concat_url: str = Field('https://functions.yandexcloud.net/d4e7lv30afsp1onahojv', env='LAMBDA_CONCAT_URL')


settings = ProjectSettings()
