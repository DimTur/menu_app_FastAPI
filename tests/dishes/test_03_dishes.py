from decimal import Decimal
from typing import Any

import pytest
from httpx import AsyncClient

from tests.menus.fixtures import test_add_and_get_one_menu
from tests.submenus.fixtures import test_add_and_get_one_submenu
from fixtures import (
    get_empty_dishes,
    post_dish,
    test_add_two_dishes,
    test_add_and_get_one_dish,
    update_dish,
)


@pytest.mark.asyncio
async def test_get_empty_dishes(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    get_empty_dishes,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == get_empty_dishes, "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_dish(
    post_dish: dict[str, str, Any],
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/"
    response = await async_client.post(
        url,
        json=post_dish,
    )

    assert response.status_code == 201, "Статус ответа не 201"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "price" in response.json(), "В ответе отсутствует price"
    assert (
        response.json()["title"] == post_dish["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == post_dish["description"]
    ), "Описание не соответствует ожидаемому"
    assert response.json()["price"] == str(
        Decimal(post_dish["price"]).quantize(Decimal("0.00"))
    ), "Цена не соответствует ожидаемой"


@pytest.mark.usefixtures("test_add_two_dishes")
async def test_get_list_dishes(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_dish_by_id(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    test_add_and_get_one_dish,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    dish = test_add_and_get_one_dish[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = await async_client.get(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json()["id"] == str(
        dish.id
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        response.json()["title"] == dish.title
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == dish.description
    ), "Описание не соответствует ожидаемому"
    assert response.json()["price"] == str(
        Decimal(dish.price).quantize(Decimal("0.00"))
    ), "Цена не соответствует ожидаемой"


@pytest.mark.asyncio
async def test_update_dish_partial(
    update_dish: dict[str, str],
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    test_add_and_get_one_dish,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    dish = test_add_and_get_one_dish[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = await async_client.patch(
        url,
        json=update_dish,
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert (
        response.json()["title"] == update_dish["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == update_dish["description"]
    ), "Описание не соответствует ожидаемому"
    assert response.json()["price"] == str(
        Decimal(update_dish["price"])
    ), "Цена не соответствует ожидаемой"
    assert "id" in response.json(), "В ответе отсутствует id"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert "price" in response.json(), "В ответе отсутствует price"


@pytest.mark.asyncio
async def test_delete_dish(
    test_add_and_get_one_menu,
    test_add_and_get_one_submenu,
    test_add_and_get_one_dish,
    async_client: AsyncClient,
):
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    dish = test_add_and_get_one_dish[0][0]
    url = f"/api/v1/menus/{menu.id}/submenus/{submenu.id}/dishes/{dish.id}"
    response = await async_client.delete(url)

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"