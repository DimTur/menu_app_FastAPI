from typing import Any

import pytest
from httpx import AsyncClient

from tests.menus.fixtures import test_add_and_get_one_menu

from .fixtures import (
    get_empty_submenus,
    post_submenu,
    test_add_and_get_one_submenu,
    test_add_two_submenus,
    update_submenu,
)


@pytest.mark.asyncio
async def test_get_empty_submenus(
    test_add_and_get_one_menu,
    get_empty_submenus,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == get_empty_submenus, "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_submenu(
    post_submenu: dict[str, Any],
    test_add_and_get_one_menu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/"
    response = await async_client.post(
        url,
        json=post_submenu,
    )

    assert response.status_code == 201, "Статус ответа не 201"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "dishes_count" in response.json(), "В ответе отсутствует dishes_count"
    assert (
        response.json()["title"] == post_submenu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == post_submenu["description"]
    ), "Описание не соответствует ожидаемому"


@pytest.mark.usefixtures("test_add_two_submenus")
async def test_get_list_submenus(
    test_add_and_get_one_menu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_submenu_by_id(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json()["id"] == str(
        submenu.id
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        response.json()["title"] == submenu.title
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == submenu.description
    ), "Описание не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_update_submenu_partial(
    update_submenu: dict[str, str],
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = await async_client.patch(
        url,
        json=update_submenu,
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()["title"] == update_submenu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == update_submenu["description"]
    ), "Описание не соответствует ожидаемому"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "dishes_count" in response.json(), "В ответе отсутствует dishes_count"


@pytest.mark.asyncio
async def test_delete_submenu(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}"
    response = await async_client.delete(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"
