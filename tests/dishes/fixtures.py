from typing import Any

import pytest
from httpx import AsyncClient
from sqlalchemy import insert, select
from sqlalchemy.engine import Result
from sqlalchemy.orm import joinedload

from core.models import Dish, Menu, Submenu, db_helper
from tests.submenus.fixtures import test_add_and_get_one_submenu


@pytest.fixture
async def get_empty_dishes(async_client: AsyncClient) -> list[Dish]:
    session = db_helper.get_scoped_session()
    query = select(Dish)
    result = await session.execute(query)
    dishes = result.all()
    await session.close()
    return dishes


@pytest.fixture
async def post_dish() -> dict[str, Any]:
    return {
        "title": "DISH1",
        "description": "DISH1 DISH1 DISH1 DISH1 DISH1",
        "price": 20.4,
    }


@pytest.fixture
async def test_add_two_dishes(
    test_add_and_get_one_submenu: Submenu,
) -> list[dict[str, Any]]:
    submenu = test_add_and_get_one_submenu[0][0]
    dishes = [
        {
            "title": "DISH1",
            "description": "DISH1DISH1DISH1DISH1",
            "submenu_id": submenu.id,
            "price": 10.88,
        },
        {
            "title": "DISH2",
            "description": "DISH2DISH2DISH2DISH2",
            "submenu_id": submenu.id,
            "price": 15.99,
        },
    ]

    session = db_helper.get_scoped_session()
    for dish in dishes:
        stmt = insert(Dish).values(**dish)
        await session.execute(stmt)
        await session.commit()

    query = select(Dish)
    result = await session.execute(query)
    dishes = result.all()
    await session.close()
    return dishes


@pytest.fixture
async def test_add_and_get_one_dish(
    test_add_and_get_one_submenu: Submenu,
) -> Dish:
    submenu = test_add_and_get_one_submenu[0][0]

    session = db_helper.get_scoped_session()

    stmt = insert(Dish).values(
        title="DISH1",
        description="DISH1DISH1DISH1DISH1",
        submenu_id=submenu.id,
        price=10.88,
    )
    await session.execute(stmt)
    await session.commit()

    query = select(Dish)
    result = await session.execute(query)
    dishes = result.all()
    await session.close()
    return dishes


@pytest.fixture
async def test_get_one_dish_by_id(
    test_add_and_get_one_menu: Menu,
    test_add_and_get_one_submenu: Submenu,
    test_add_and_get_one_dish: Dish,
) -> Dish:
    session = db_helper.get_scoped_session()
    menu_id = test_add_and_get_one_menu[0][0].id
    submenu_id = test_add_and_get_one_submenu[0][0].id
    dish_id = test_add_and_get_one_dish[0][0].id
    stmt = (
        select(Dish)
        .join(Dish.submenu)
        .join(Submenu.menu)
        .options(joinedload(Dish.submenu).joinedload(Submenu.menu))
        .where(Menu.id == menu_id)
        .where(Submenu.id == submenu_id)
        .where(Dish.id == dish_id)
    )
    result: Result = await session.execute(stmt)
    dish = result.scalar()
    await session.close()
    return dish


@pytest.fixture
async def update_dish() -> dict[str, Any]:
    return {
        "title": "NEW DISH",
        "description": "NEW DISH NEW DISH NEW DISH NEW DISH",
        "price": 40,
    }
