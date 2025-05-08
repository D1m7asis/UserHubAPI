def test_get_nonexistent_user(client, unknown_user_id):
    response = client.get(f"/users/{unknown_user_id}")
    assert response.status_code == 404
    assert response.json()["message"] == f"User with ID {unknown_user_id} not found"


def test_update_nonexistent_user(client, unknown_user_id):
    response = client.patch(f"/users/{unknown_user_id}", json={"name": "Test"})
    assert response.status_code == 404


def test_create_user_invalid_payload(client):
    response = client.post("/users", json={"invalid": "data"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in response.json()
    assert "Validation failed" in data["detail"]


def test_delete_nonexistent_user(client, unknown_user_id):
    response = client.delete(f"/users/{unknown_user_id}")
    assert response.status_code == 404


def test_unknown_route_error(monkeypatch, client):
    response = client.get("/not_users")
    assert response.status_code == 404
