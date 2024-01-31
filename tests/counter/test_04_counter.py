from decimal import Decimal
from typing import Any

import pytest
from httpx import AsyncClient

from tests.menus.fixtures import (
    test_add_and_get_one_menu,
    test_get_one_menu_by_id,
)
from tests.submenus.fixtures import (
    test_add_and_get_one_submenu,
    test_get_one_submenu_by_id,
)
from tests.dishes.fixtures import (
    get_empty_dishes,
    post_dish,
    test_add_two_dishes,
    test_add_and_get_one_dish,
    update_dish,
)


@pytest.mark.usefixtures("test_add_two_dishes")
async def test_get_menu_by_id(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    test_get_one_menu_by_id,
    async_client: AsyncClient,
):
    menu = test_get_one_menu_by_id
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
    assert response.json()["submenus_count"] == len(
        menu.submenus
    ), "Количество подменю не соответствует ожидаемому"
    assert response.json()["dishes_count"] == sum(
        len(submenu.dishes) for submenu in menu.submenus
    ), "Количество блюд не соответствует ожидаемому"


@pytest.mark.usefixtures("test_add_two_dishes")
async def test_get_submenu_by_id(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    test_get_one_menu_by_id,
    test_get_one_submenu_by_id,
    async_client: AsyncClient,
):
    menu = test_get_one_menu_by_id
    submenu = test_get_one_submenu_by_id
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
    assert response.json()["dishes_count"] == len(
        submenu.dishes
    ), "Количество блюд не соответствует ожидаемому"
