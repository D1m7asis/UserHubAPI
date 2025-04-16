def test_create_user(client, user_data):
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == user_data["name"]
    assert data["surname"] == user_data["surname"]
    assert "id" in data
    assert "password" not in data


def test_get_users(client, user_data):
    # Создаем пользователя
    client.post("/users/", json=user_data)

    # Получаем список
    response = client.get("/users/")
    assert response.status_code == 200
    users = response.json()["data"]
    assert isinstance(users, list)
    assert len(users) > 0
    assert all("password" not in user for user in users)


def test_get_user(client, user_data):
    # Создаем пользователя
    create_res = client.post("/users/", json=user_data)
    user_id = create_res.json()["data"]["id"]

    # Получаем одного
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()["data"]
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]


def test_update_user(client, user_data):
    # Создаем пользователя
    create_res = client.post("/users/", json=user_data)
    user_id = create_res.json()["data"]["id"]

    # Обновляем
    update_data = {"name": "Updated"}
    response = client.patch(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "Updated"


def test_delete_user(client, user_data):
    # Создаем пользователя
    create_res = client.post("/users/", json=user_data)
    user_id = create_res.json()["data"]["id"]

    # Удаляем
    delete_res = client.delete(f"/users/{user_id}")
    assert delete_res.status_code == 204

    # Проверяем что удалился
    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 404
