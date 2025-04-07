import asyncio
import os

import pytest
from alembic.command import upgrade
from alembic.config import Config
from litestar.testing import TestClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from src.app.asgi import app


@pytest.fixture(scope="session", autouse=True)
def event_loop():
    """Главный event loop для всех асинхронных тестов"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Фикстура тестового клиента"""

    with TestClient(app=app) as client:
        yield client


@pytest.fixture(scope="module")
def user_data() -> dict[str, str]:
    """Тестовые данные пользователя"""
    return {
        "name": "Test",
        "surname": "User",
        "password": "TestPass123"
    }


@pytest.fixture(scope="session", autouse=True)
async def apply_migrations():
    """Применяем миграции перед тестами"""
    db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/test_db")
    engine = create_async_engine(db_url)

    # Проверка соединения
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    # Применяем миграции
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", db_url)
    upgrade(alembic_cfg, "head")
    await engine.dispose()
