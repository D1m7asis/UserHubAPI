import pytest
from litestar.testing import AsyncTestClient

from src.app.asgi import app  # Импортируем ваше приложение Litestar


@pytest.fixture
async def client() -> AsyncTestClient:
    """Фикстура, предоставляющая тестовый клиент для каждого теста"""
    async with AsyncTestClient(app=app) as client:
        yield client


@pytest.fixture
def user_data() -> dict[str, str]:
    """Фикстура с тестовыми данными пользователя"""
    return {
        "name": "Test",
        "surname": "User",
        "password": "testpass123"
    }


@pytest.mark.asyncio
async def test_delete_user(client: AsyncTestClient, user_data: dict[str, str]):
    """
    Тестирование полного цикла:
    1. Создание пользователя
    2. Удаление пользователя
    3. Проверка что пользователь удален
    """
    # Шаг 1: Создание пользователя
    create_response = await client.post(
        "/users/",
        json=user_data
    )
    assert create_response.status_code == 201
    created_user = create_response.json()
    user_id = created_user["id"]

    # Шаг 2: Удаление пользователя
    delete_response = await client.delete(f"/users/{user_id}")

    # Проверки для удаления
    assert delete_response.status_code == 204
    assert not delete_response.content  # Проверяем что тело ответа пустое

    # Шаг 3: Проверка что пользователь действительно удален
    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
    error_detail = get_response.json()
    assert error_detail["detail"] == "User not found"
