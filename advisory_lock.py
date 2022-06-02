import asyncio

import asyncpg
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import create_async_engine

DATABASE_URI = "postgresql+asyncpg://postgres:postgres@localhost/test"
DATABASE_DSN = "postgresql://postgres:postgres@localhost/test"
MAX_LOCK_ID_32: int = 2**31 - 1
MAX_LOCK_ID_64: int = 2**63 - 1
LOCK_ID = MAX_LOCK_ID_64


async def use_asyncpg() -> None:
    conn = await asyncpg.connect(dsn=DATABASE_DSN)

    try:
        async with conn.transaction():
            stmt = await conn.prepare(
                "SELECT pg_advisory_xact_lock($1::bigint) AS pg_advisory_xact_lock_1"
            )
            await stmt.fetchval(LOCK_ID)
    finally:
        await conn.close()


async def use_sqlalchemy() -> None:
    engine = create_async_engine(DATABASE_URI)

    try:
        async with engine.begin() as conn:
            query = select(func.pg_advisory_xact_lock(LOCK_ID))

            await conn.execute(query)

    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(use_asyncpg())
    asyncio.run(use_sqlalchemy())
