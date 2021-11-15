from logging import config as logging_config
from typing import Any, Dict, Optional

from pydantic import BaseSettings, Field, PostgresDsn, validator

from .logger import LOGGING

logging_config.dictConfig(LOGGING)


class PostgresDsnWithAsync(PostgresDsn):
    """ hack """
    allowed_schemes = {'postgres', 'postgresql', 'postgresql+asyncpg'}


class DataBaseSettings(BaseSettings):
    host: str = Field("localhost", env="POSTGRES_HOST")
    port: str = Field('5432', env="POSTGRES_PORT")
    name: str = Field("bot", env="POSTGRES_DB")
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


class ProjectSettings(BaseSettings):
    project_name: str = "Dude Bot"
    debug: bool = Field(True, env="BOT_DEBUG")
    test: bool = Field(False, env="BOT_TEST")
    database = DataBaseSettings()


settings = ProjectSettings()
