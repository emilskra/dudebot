#! /usr/bin/env python3
import logging
import asyncio
import os

import ydb
from ydb.table import BaseSession
from core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PACKS_DATA = os.getenv('PACKS_DATA', 'dev')
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', PACKS_DATA)


async def clean_db(session: BaseSession):
    for table in ("packs", "interviews"):
        session.drop_table(table)


async def async_main() -> None:
    driver_config = ydb.DriverConfig(
        settings.database_url,
        settings.database_name,
        credentials=ydb.construct_credentials_from_environ(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )
    with ydb.Driver(driver_config) as driver:
        driver.wait(timeout=10)
        session = driver.table_client.session().create()
        logger.info("cleaning old data")
        await clean_db(session)

        logger.info("creating tables")
        await create_interview_table(session, settings.database_name)
        await create_packs_table(session, settings.database_name)

        logger.info("tables created")


if __name__ == "__main__":
    asyncio.run(async_main())
