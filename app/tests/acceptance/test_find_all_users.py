import pytest
from httpx import AsyncClient, ASGITransport

from api.demo.internal.config import get_settings

from api.main import app

settings = get_settings()


@pytest.mark.asyncio
async def test_get_users():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    ) as client:
        response = await client.get(f"{settings.PREFIX}/users")
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"
        assert response.json() == [{"username": "johndoe"}, {"username": "janedoe"}]
