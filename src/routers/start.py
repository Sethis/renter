

from contextlib import asynccontextmanager

from src.database.structure.model import Base
from src.di.db import engine


@asynccontextmanager
async def init_models(*_args):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield 
