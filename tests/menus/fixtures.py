import pytest
from httpx import AsyncClient
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result

from core.models import db_helper, Menu, Submenu


@pytest.fixture
async def get_empty_menus(async_client: AsyncClient):
    session = db_helper.get_scoped_session()
    query = select(Menu)
    result = await session.execute(query)
    menus = result.all()
    await session.close()
    return menus


@pytest.fixture
async def post_menu() -> dict[str, str]:
    return {
        "title": "menu1",
        "description": "1111111111111",
    }


@pytest.fixture
async def test_add_two_menus():
    menus = [
        {"title": "MENU1", "description": "MENU1MENU1MENU1MENU1MENU1"},
        {"title": "MENU2", "description": "MENU2MENU2MENU2MENU2MENU2"},
    ]

    session = db_helper.get_scoped_session()
    for menu in menus:
        stmt = insert(Menu).values(**menu)
        await session.execute(stmt)
        await session.commit()


@pytest.fixture
async def test_add_and_get_one_menu():
    session = db_helper.get_scoped_session()
    stmt = insert(Menu).values(title="MENU1", description="MENU1MENU1MENU1MENU1MENU1")
    await session.execute(stmt)
    await session.commit()

    query = select(Menu)
    result = await session.execute(query)
    menus = result.all()
    await session.close()
    return menus


@pytest.fixture
async def test_get_one_menu_by_id(
    test_add_and_get_one_menu,
):
    session = db_helper.get_scoped_session()
    menu_id = test_add_and_get_one_menu[0][0].id
    stmt = (
        select(Menu)
        .filter(Menu.id == menu_id)
        .options(selectinload(Menu.submenus).selectinload(Submenu.dishes))
    )
    result: Result = await session.execute(stmt)
    menu = result.scalar()
    await session.close()
    return menu


@pytest.fixture
async def update_menu() -> dict[str, str]:
    return {
        "title": "NEW MENU",
        "description": "NEW NEW NEW NEW NEW",
    }
