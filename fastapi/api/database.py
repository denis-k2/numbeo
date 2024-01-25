from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

RELOHELPER_URL = settings.relohelper_url
RELOHELPER_ASYNC_URL = settings.relohelper_async_url

engine = create_engine(RELOHELPER_URL)
async_engine = create_async_engine(RELOHELPER_ASYNC_URL)
async_session = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    async with async_session() as session:
        yield session
