import pytest
from httpx import AsyncClient

from api_v1.menus.views import get_menu_by_id
from api_v1.submenus.views import get_submenu_bu_id
from tests.dishes.fixtures import test_add_two_dishes
from tests.menus.fixtures import test_add_and_get_one_menu, test_get_one_menu_by_id
from tests.service import reverse
from tests.submenus.fixtures import (
    test_add_and_get_one_submenu,
    test_get_one_submenu_by_id,
)


@pytest.mark.usefixtures("test_add_two_dishes")
async def test_get_menu_by_id(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    test_get_one_menu_by_id,
    async_client: AsyncClient,
):
    menu = test_get_one_menu_by_id
    response = await async_client.get(reverse(get_menu_by_id, menu_id=menu.id))

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
    assert response.json()["dishes_count"] == len(
        submenu.dishes
    ), "Количество блюд не соответствует ожидаемому"
