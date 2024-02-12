from decimal import Decimal

import pytest
from httpx import AsyncClient

from api_v1.dishes.schemas import Dish
from api_v1.menus.schemas import Menu
from api_v1.menus.views import (
    create_menu,
    delete_menu,
    get_all_base,
    get_menu_by_id,
    get_menus,
    update_menu_partial,
)
from api_v1.submenus.schemas import Submenu
from tests.conftest import async_client
from tests.dishes.fixtures import test_add_and_get_one_dish, test_get_one_dish_by_id
from tests.service import reverse
from tests.submenus.fixtures import (
    test_add_and_get_one_submenu,
    test_get_one_submenu_by_id,
)

from .fixtures import (
    get_empty_menus,
    post_menu,
    test_add_and_get_one_menu,
    test_add_two_menus,
    test_get_one_menu_by_id,
    update_menu,
)


@pytest.mark.asyncio
async def test_get_empty_menus(
    get_empty_menus: list[Menu],
    async_client: AsyncClient,
) -> None:
    response = await async_client.get(reverse(get_menus))

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() == get_empty_menus, "В ответе не пустой список"


@pytest.mark.asyncio
async def test_add_menu(
    post_menu: dict[str, str],
    async_client: AsyncClient,
) -> None:
    response = await async_client.post(
        reverse(create_menu),
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
async def test_get_menus(async_client: AsyncClient) -> None:
    response = await async_client.get(reverse(get_menus))

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() != [], "В ответе пустой список"


@pytest.mark.asyncio
async def test_get_menu_by_id(
    test_add_and_get_one_menu: Menu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    response = await async_client.get(
        reverse(
            get_menu_by_id,
            menu_id=menu.id,
        )
    )

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
    test_add_and_get_one_menu: Menu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    response = await async_client.patch(
        reverse(
            update_menu_partial,
            menu_id=menu.id,
        ),
        json=update_menu,
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert "title" in response.json(), "В ответе отсутствует title"
    assert "description" in response.json(), "В ответе отсутствует description"
    assert (
        response.json()["title"] == update_menu["title"]
    ), "Название не соответствует ожидаемому"
    assert (
        response.json()["description"] == update_menu["description"]
    ), "Описание не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_delete_menu(
    test_add_and_get_one_menu: Menu,
    async_client: AsyncClient,
) -> None:
    menu = test_add_and_get_one_menu[0][0]
    response = await async_client.delete(
        reverse(
            delete_menu,
            menu_id=menu.id,
        )
    )

    assert response.status_code == 200, "Статус ответа не 200"
    assert response.json() is None, "Сообщение об удалении не соответствует ожидаемому"


@pytest.mark.asyncio
async def test_get_all_menus(
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    test_add_and_get_one_dish: Dish,
    test_get_one_menu_by_id: Menu,
    test_get_one_submenu_by_id: Submenu,
    test_get_one_dish_by_id: Dish,
    async_client: AsyncClient,
) -> None:
    menu = test_get_one_menu_by_id
    submenu = test_get_one_submenu_by_id
    dish = test_get_one_dish_by_id
    response = await async_client.get(reverse(get_all_base))

    assert response.status_code == 200, "Статус ответа не 200"

    menu_response = response.json()[0]
    assert menu_response["id"] == str(
        menu.id
    ), "Идентификатор не соответствует ожидаемому"
    assert menu_response["title"] == menu.title, "Название не соответствует ожидаемому"
    assert (
        menu_response["description"] == menu.description
    ), "Описание не соответствует ожидаемому"

    submenu_response = response.json()[0]["submenus"][0]
    assert submenu_response["id"] == str(
        submenu.id
    ), "Идентификатор не соответствует ожидаемому"
    assert (
        submenu_response["title"] == submenu.title
    ), "Название не соответствует ожидаемому"
    assert (
        submenu_response["description"] == submenu.description
    ), "Описание не соответствует ожидаемому"

    dish_response = response.json()[0]["submenus"][0]["dishes"][0]
    assert dish_response["id"] == str(
        dish.id
    ), "Идентификатор не соответствует ожидаемому"
    assert dish_response["title"] == dish.title, "Название не соответствует ожидаемому"
    assert (
        dish_response["description"] == dish.description
    ), "Описание не соответствует ожидаемому"
    assert dish_response["price"] == str(
        Decimal(dish.price).quantize(Decimal("0.00"))  # type: ignore
    ), "Цена не соответствует ожидаемому"
