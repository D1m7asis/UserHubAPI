import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv(
    key="DATABASE_URL",
    default="postgresql+asyncpg://user:password@localhost:5432/users_db"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Включаем логирование SQL-запросов
    pool_pre_ping=True  # Проверяем соединение перед использованием
)

# Асинхронная сессия
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as session:
        yield session
