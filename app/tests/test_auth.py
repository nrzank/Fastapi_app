import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user():

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/api/v1/register/", json={"email": "asapnrz@gmail.com", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_user():

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post("/api/v1/register/", json={"email": "asapnrz@gmail.com", "password": "1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    return response.json()["access_token"]
