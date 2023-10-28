

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.actions.logic import Logic
from src.config.config_reader import config


engine = create_async_engine(
    config.db_url,
    echo=False,
    pool_size=15,
    max_overflow=15,
    connect_args={
        "server_settings": {"jit": "off"}
    }
)

sessionmaker = async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with sessionmaker() as session:
        yield session


async def get_logic(session: Annotated[AsyncSession, Depends(get_session)]) -> Logic:
    return Logic(session)
