def test_get_nonexistent_user(client):
    response = client.get("/users/999999")
    assert response.status_code == 404
    assert response.json()["code"] == "user_not_found"


def test_update_nonexistent_user(client):
    response = client.patch("/users/999999", json={"name": "Test"})
    assert response.status_code == 404


def test_create_user_invalid_payload(client):
    response = client.post("/users", json={"invalid": "data"})
    assert response.status_code == 400
    data = response.json()
    assert "detail" in response.json()
    assert "Validation failed" in data["detail"]


def test_unknown_route_error(monkeypatch, client):
    response = client.get("/not_users")
    assert response.status_code == 404


def test_delete_nonexistent_user(client):
    response = client.delete("/users/999999")
    assert response.status_code == 404
