from databases import Database
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from config import TAGGING_POSTGRES_DB, TAGGING_POSTGRES_USER, TAGGING_POSTGRES_PASSWORD

DATABASE_URL = f"postgresql+asyncpg://{TAGGING_POSTGRES_USER}:{TAGGING_POSTGRES_PASSWORD}@tagging-db:5432/{TAGGING_POSTGRES_DB}"
# print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
metadata = MetaData()

# For synchronous operations, mainly migrations
sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", ""))

async def get_db():
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session