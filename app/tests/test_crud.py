import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def get_token():
    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post(
            "/api/v1/register/", json={"email": "asapnrz@gmail.com", "password": "1234"}
        )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_department():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post(
            "/api/v1/department/", json={"name": "Pr"}, headers=headers
        )

    assert response.status_code == 200
    assert response.json()["name"] == "Pr"


@pytest.mark.asyncio
async def test_create_officer():
    token = await get_token()
    headers = {"Authorization": f"Bearer {token}"}

    async with AsyncClient(base_url="http://localhost:8000") as ac:
        response = await ac.post(
            "/api/v1/officer/",
            json={
                "first_name": "Nurzhan",
                "last_name": "Kumarov",
                "email": "kumaroff02@gmail.com",
                "department_id": 1,
            },
            headers=headers,
        )

    assert response.status_code == 200
    assert response.json()["email"] == "kumaroff02@gmail.com"
