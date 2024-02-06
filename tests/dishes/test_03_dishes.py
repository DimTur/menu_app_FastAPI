from decimal import Decimal
from typing import Any

import pytest
from httpx import AsyncClient

from api_v1.dishes.schemas import Dish
from api_v1.dishes.views import (
    create_dish,
    delete_dish,
    get_dish_by_id,
    get_dishes,
    update_dish_partial,
)
from api_v1.menus.schemas import Menu
from api_v1.submenus.schemas import Submenu
from tests.menus.fixtures import test_add_and_get_one_menu
from tests.service import reverse
from tests.submenus.fixtures import test_add_and_get_one_submenu

from .fixtures import (
    get_empty_dishes,
    post_dish,
    test_add_and_get_one_dish,
    test_add_two_dishes,
    update_dish,
)


@pytest.mark.asyncio
async def test_get_empty_dishes(
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    get_empty_dishes: list[Dish],
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    response = await async_client.get(
        reverse(
            get_dishes,
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == get_empty_dishes, "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_dish(
    post_dish: dict[str, Any],
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    response = await async_client.post(
        reverse(
            create_dish,
            menu_id=menu.id,
            submenu_id=submenu.id,
        ),
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
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    response = await async_client.get(
        reverse(
            get_dishes,
            menu_id=menu.id,
            submenu_id=submenu.id,
        )
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_dish_by_id(
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    test_add_and_get_one_dish: Dish,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    dish = test_add_and_get_one_dish[0][0]
    response = await async_client.get(
        reverse(
            get_dish_by_id,
            menu_id=menu.id,
            submenu_id=submenu.id,
            dish_id=dish.id,
        )
    )
    assert response.status_code == 200, "Статус ответа не 200"
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
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    test_add_and_get_one_dish: Dish,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    dish = test_add_and_get_one_dish[0][0]
    response = await async_client.patch(
        reverse(
            update_dish_partial,
            menu_id=menu.id,
            submenu_id=submenu.id,
            dish_id=dish.id,
        ),
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
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    test_add_and_get_one_dish: Dish,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    submenu = test_add_and_get_one_submenu[0][0]
    dish = test_add_and_get_one_dish[0][0]
    response = await async_client.delete(
        reverse(
            delete_dish,
            menu_id=menu.id,
            submenu_id=submenu.id,
            dish_id=dish.id,
        )
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"
