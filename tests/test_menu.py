from typing import Any

import pytest
from httpx import AsyncClient

from conftest import async_client
from fixtures import post_menu, saved_data


@pytest.mark.asyncio
async def test_get_empty_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_add_menu(
    post_menu: dict[str, str],
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/api/v1/menus/",
        json=post_menu,
    )

    assert response.status_code == 201
    assert response.json()["title"] == post_menu["title"]
    assert response.json()["description"] == post_menu["description"]

    menu_id = response.json()["id"]
    assert menu_id is not None
    assert isinstance(menu_id, str)

    saved_data["menu"] = response.json()


@pytest.mark.asyncio
async def test_get_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200
    assert response.json() != []


@pytest.mark.asyncio
async def test_get_menu_by_id(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    response = await async_client.get(
        "/api/v1/menus/",
        params={"id": menu["id"]},
    )

    assert response.status_code == 200
    assert response.json()[0]["id"] == menu["id"]
    assert response.json()[0]["title"] == menu["title"]
    assert response.json()[0]["description"] == menu["description"]
