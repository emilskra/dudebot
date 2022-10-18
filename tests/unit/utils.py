from sqlalchemy import insert


async def db_inserts(db, payload: dict):
    if not payload:
        return
    async with db.begin() as conn:
        for table, values in payload.items():
            await conn.execute(insert(table).values(values))
