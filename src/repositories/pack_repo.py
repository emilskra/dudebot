import ydb

from schemas.pack_schema import Pack


class PackRepo:
    def __init__(self, session_pool: ydb.aio.SessionPool):
        self.session_pool = session_pool

    async def add_packs(self, packs: list[Pack]):
        async def execute(session):
            query = """
            DECLARE $packsData AS List<Struct<
                id: String,
                name: String,
                intro_file: String,
                outro_file: String>>;
            INSERT INTO packs
            SELECT
                id,
                name,
                intro_file,
                outro_file
            FROM AS_TABLE($packsData);
            """
            prepared_query = await session.prepare(query)
            await session.transaction().execute(
                prepared_query,
                parameters={
                    "$packsData": packs,
                },
                commit_tx=True,
            )

        await self.session_pool.retry_operation(execute)

    async def get_pack(self, pack_id: int) -> Pack:
        ...

    async def get_all_packs(self) -> list[dict]:
        async def execute(session):
            query = """
                SELECT name FROM packs;
            """
            prepared_query = await session.prepare(query)
            return await session.execute(prepared_query)

        return await self.session_pool.retry_operation(execute)

    async def get_user_pack(self, user_id: int):
        ...
