import os.path
from typing import Optional

from pydantic import BaseSettings, Field, validator


class BotSettings(BaseSettings):
    token: Optional[str]
    webhook_path: Optional[str] = None
    webhook_url: Optional[str] = None


class YDBSettings(BaseSettings):
    database_host: str = Field("grpc://localhost:2136")
    database_name: str = Field("/local")


class PostgresSQLSettings(BaseSettings):
    database_host: str = Field("postgresql+asyncpg://bot:dudebot@localhost:5436")
    database_uri: str = Field("postgresql+asyncpg://bot:dudebot@localhost:5436/dudebot")
    pg_connect_timeout: int = Field(
        30, description="PostgreSQL connect timeout in seconds"
    )
    pg_echo_enabled: bool = Field(False, description="Logging enabled")
    pg_pool_max_size: int = Field(30, description="PostgreSQL pool max size")
    pg_pool_timeout: int = Field(60, description="PostgreSQL pool timeout")
    pg_pool_recycle: int = Field(
        -1, description="PostgreSQL pool recycle in sec. Use -1 to disable pool recycle"
    )
    pg_pool_pre_ping: bool = Field(
        True,
        description="The connection is transparently re-connected and upon success",
    )


class ProjectSettings(BaseSettings):
    project_name: str = "Dude Bot"
    base_dir: str = os.path.dirname(os.path.dirname(__file__))
    debug: bool = Field(False, env="BOT_DEBUG")
    port: int = Field(9000)
    lambda_concat_url: str = Field(
        "https://functions.yandexcloud.net/d4e7lv30afsp1onahojv"
    )

    database: PostgresSQLSettings = PostgresSQLSettings()
    bot: BotSettings = BotSettings()

    class Config:
        env_file = ".env"


settings = ProjectSettings()
