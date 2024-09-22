import os

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "user")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_DB = os.getenv("POSTGRES_DB", "db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

DSN = (f"postgresql+asyncpg://{POSTGRES_USER}:"
       f"{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
       f"{POSTGRES_PORT}/{POSTGRES_DB}")


engine = create_async_engine(DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    pass


async def init_db():
    """Database initialization"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
