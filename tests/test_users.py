import pytest


@pytest.mark.asyncio
async def test_create_user(client, user_data):
    response = await client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert "id" in data
    assert "created_at" in data
    assert "password" not in data  # Пароль не должен возвращаться


@pytest.mark.asyncio
async def test_get_users(client, user_data):
    # Сначала создаем пользователя
    await client.post("/users/", json=user_data)

    # Получаем список
    response = await client.get("/users/")
    assert response.status_code == 200
    users = response.json()
    assert isinstance(users, list)
    assert len(users) > 0
    assert all("password" not in user for user in users)


@pytest.mark.asyncio
async def test_get_user(client, user_data):
    # Создаем пользователя
    create_res = await client.post("/users/", json=user_data)
    user_id = create_res.json()["id"]

    # Получаем одного
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]


@pytest.mark.asyncio
async def test_update_user(client, user_data):
    # Создаем пользователя
    create_res = await client.post("/users/", json=user_data)
    user_id = create_res.json()["id"]

    # Обновляем
    update_data = {"name": "Updated"}
    response = await client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


@pytest.mark.asyncio
async def test_delete_user(client, user_data):
    # Создаем пользователя
    create_res = await client.post("/users/", json=user_data)
    user_id = create_res.json()["id"]

    # Удаляем
    delete_res = await client.delete(f"/users/{user_id}")
    assert delete_res.status_code == 204

    # Проверяем что удалился
    get_res = await client.get(f"/users/{user_id}")
    assert get_res.status_code == 404
