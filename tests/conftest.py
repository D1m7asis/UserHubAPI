import asyncio

import pytest
from litestar.testing import TestClient

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
