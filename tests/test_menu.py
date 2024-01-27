from typing import Any

import pytest
from httpx import AsyncClient

from conftest import async_client
from fixtures import (
    post_menu,
    update_menu,
    saved_data,
)


@pytest.mark.asyncio
async def test_get_empty_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == [], "В ответе не пустой список"


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

    assert response.status_code == 201, "Статус ответа не 201"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "submenus_count" in response.json(), "В ответе отсутствует submenus_count"
    assert "dishes_count" in response.json(), "В ответе отсутствует dishes_count"
    assert (
        response.json()["title"] == post_menu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == post_menu["description"]
    ), "Описание не соответствует ожидаемому"

    menu_id = response.json()["id"]
    assert menu_id is not None
    assert isinstance(menu_id, str)

    saved_data["menu"] = response.json()


@pytest.mark.asyncio
async def test_get_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


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

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()[0]["id"] == menu["id"]
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        response.json()[0]["title"] == menu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()[0]["description"] == menu["description"]
    ), "Описание не соответствует ожидаемому"
    assert (
        response.json()[0]["submenus_count"] == menu["submenus_count"]
    ), "Количество подменю не соответствует ожидаемому"
    assert (
        response.json()[0]["dishes_count"] == menu["dishes_count"]
    ), "Количество блюд не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_update_menu_partial(
    update_menu: dict[str, str],
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    url = f"/api/v1/menus/{menu['id']}"
    response = await async_client.patch(
        url,
        json=update_menu,
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()["title"] == update_menu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == update_menu["description"]
    ), "Описание не соответствует ожидаемому"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "submenus_count" in response.json(), "В ответе отсутствует submenus_count"
    assert "dishes_count" in response.json(), "В ответе отсутствует dishes_count"


# @pytest.mark.asyncio
# async def test_delete_menu(
#     saved_data: dict[str, Any],
#     async_client: AsyncClient,
# ):
#     menu = saved_data["menu"]
#     url = f"/api/v1/menus/{menu['id']}"
#     print(url)
#     response = await async_client.delete(url)
#
#     print(response)
#     # assert response.status_code == 200
#     # assert response.json()[0]["id"] == menu["id"]
#     # assert response.json()[0]["title"] == menu["title"]
#     # assert response.json()[0]["description"] == menu["description"]
