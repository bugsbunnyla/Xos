import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/auth/register", json={
            "email": "test@example.com",
            "password": "testpassword123",
            "first_name": "Test",
            "last_name": "User"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
