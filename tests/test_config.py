def test_delete_user(client, user_data):
    """
    Синхронное тестирование цикла удаления пользователя:
    1. Создание
    2. Удаление
    3. Проверка удаления
    """
    # Шаг 1: Создание пользователя
    create_response = client.post(
        "/users/",
        json=user_data
    )
    assert create_response.status_code == 201
    user_id = create_response.json()["data"]["id"]

    # Шаг 2: Удаление пользователя
    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200

    # Шаг 3: Проверка удаления
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
    assert get_response.json()["status"] == "error"
    assert get_response.json()["message"] == f"User with ID {user_id} not found"
