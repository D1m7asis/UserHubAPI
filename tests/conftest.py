import pytest
from litestar.testing import TestClient

from src.app.asgi import app


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


@pytest.fixture(scope="module")
def unknown_user_id() -> int:
    """Тестовые данные пользователя"""
    return 99999999999
