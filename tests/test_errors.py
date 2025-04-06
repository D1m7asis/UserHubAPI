import pytest


@pytest.mark.asyncio
async def test_nonexistent_user(client):
    response = await client.get("/users/999999")
    assert response.status_code == 404
    assert "detail" in response.json()


@pytest.mark.asyncio
async def test_update_nonexistent_user(client):
    response = await client.patch("/users/999999", json={"name": "Test"})
    assert response.status_code == 404
