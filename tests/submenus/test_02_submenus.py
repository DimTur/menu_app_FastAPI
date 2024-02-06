from typing import Any

import pytest
from httpx import AsyncClient

from api_v1.menus.schemas import Menu
from api_v1.submenus.schemas import Submenu
from api_v1.submenus.views import (
    create_submenu,
    delete_submenu,
    get_submenu_bu_id,
    get_submenus,
    update_submenu_partial,
)
from tests.menus.fixtures import test_add_and_get_one_menu
from tests.service import reverse

from .fixtures import (
    get_empty_submenus,
    post_submenu,
    test_add_and_get_one_submenu,
    test_add_two_submenus,
    update_submenu,
)


@pytest.mark.asyncio
async def test_get_empty_submenus(
    test_add_and_get_one_menu: Menu,
    get_empty_submenus: list[Submenu],
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    response = await async_client.get(
        reverse(
            get_submenus,
            menu_id=menu.id,
        )
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == get_empty_submenus, "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_submenu(
    post_submenu: dict[str, Any],
    test_add_and_get_one_menu: Menu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    response = await async_client.post(
        reverse(
            create_submenu,
            menu_id=menu.id,
        ),
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
    test_add_and_get_one_menu: Menu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_submenu_by_id(
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    response = await async_client.get(
        reverse(
            get_submenu_bu_id,
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
    )

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
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    response = await async_client.patch(
        reverse(
            update_submenu_partial,
            menu_id=menu.id,
            submenu_id=submenu.id,
        ),
        json=update_submenu,
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()["title"] == update_submenu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == update_submenu["description"]
    ), "Описание не соответствует ожидаемому"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"


@pytest.mark.asyncio
async def test_delete_submenu(
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    response = await async_client.delete(
        reverse(
            delete_submenu,
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"
