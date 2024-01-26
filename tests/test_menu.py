import pytest
from httpx import AsyncClient

from conftest import async_client


@pytest.mark.asyncio
async def test_add_menu(async_client: AsyncClient):
    response = await async_client.post(
        "/api/v1/menus/",
        json={
            "title": "menu2",
            "description": "1111111111111111111",
        },
    )

    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200


# def test_1():
#     assert 1 == 1
