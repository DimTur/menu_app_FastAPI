from typing import Any

import pytest
from httpx import AsyncClient

from fixtures import (
    post_menu,
    saved_data,
    post_submenu,
    update_submenu,
)


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
async def test_get_empty_submenus(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == [], "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_submenu(
    post_submenu: dict[str, Any],
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/"
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

    saved_data["submenu"] = response.json()


@pytest.mark.asyncio
async def test_get_list_submenus(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_submenu_by_id(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()["id"] == submenu["id"]
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        response.json()["title"] == submenu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == submenu["description"]
    ), "Описание не соответствует ожидаемому"
    assert (
        response.json()["dishes_count"] == submenu["dishes_count"]
    ), "Количество блюд не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_update_submenu_partial(
    update_submenu: dict[str, str],
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}"
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

    saved_data["submenu"] = response.json()


@pytest.mark.asyncio
async def test_get_updated_submenu_by_id(
    update_submenu: dict[str, str],
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()["id"] == submenu["id"]
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        response.json()["title"] == submenu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == submenu["description"]
    ), "Описание не соответствует ожидаемому"
    assert (
        response.json()["dishes_count"] == submenu["dishes_count"]
    ), "Количество блюд не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_delete_submenu(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}"
    response = await async_client.delete(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_get_new_empty_submenus(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == [], "В ответе не пустой список"


@pytest.mark.asyncio
async def test_get_deleted_submenu_by_id(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    url = f"/api/v1/menus/{menu['id']}/submenus/{submenu['id']}"
    response = await async_client.delete(url)

    assert response.status_code == 404, "Статус ответа не 404"
    assert (
        response.json()["detail"] == "submenu not found"
    ), "Сообщение об ошибке не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_delete_menu(
    saved_data: dict[str, Any],
    async_client: AsyncClient,
):
    menu = saved_data["menu"]
    url = f"/api/v1/menus/{menu['id']}"
    response = await async_client.delete(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_get_empty_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == [], "В ответе не пустой список"
