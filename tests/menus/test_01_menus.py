import pytest
from httpx import AsyncClient

from tests.conftest import async_client

from fixtures import (
    get_empty_menus,
    post_menu,
    test_add_and_get_one_menu,
    test_add_two_menus,
    update_menu,
)


@pytest.mark.asyncio
async def test_get_empty_menus(
    get_empty_menus,
    async_client: AsyncClient,
):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == get_empty_menus, "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_menu(
    post_menu: dict[str, str],
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


@pytest.mark.usefixtures("test_add_two_menus")
async def test_get_menus(async_client: AsyncClient):
    response = await async_client.get(
        "/api/v1/menus/",
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_menu_by_id(
    test_add_and_get_one_menu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json()["id"] == str(
        menu.id
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        response.json()["title"] == menu.title
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == menu.description
    ), "Описание не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_update_menu_partial(
    update_menu: dict[str, str],
    test_add_and_get_one_menu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}"
    response = await async_client.patch(
        url,
        json=update_menu,
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "submenus_count" in response.json(), "В ответе отсутствует submenus_count"
    assert "dishes_count" in response.json(), "В ответе отсутствует dishes_count"
    assert (
        response.json()["title"] == update_menu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == update_menu["description"]
    ), "Описание не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_delete_menu(
    test_add_and_get_one_menu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}"
    response = await async_client.delete(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"
