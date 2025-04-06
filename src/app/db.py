import os

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    key="DATABASE_URL",
    default="postgresql+asyncpg://user:password@localhost:5432/users_db"
)

engine = create_async_engine(DATABASE_URL)
SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
