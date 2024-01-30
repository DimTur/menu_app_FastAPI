import pytest
from httpx import AsyncClient
from sqlalchemy import select, insert

from core.models import db_helper, Submenu
from tests.menus.fixtures import test_add_and_get_one_menu


@pytest.fixture
async def get_empty_submenus(async_client: AsyncClient):
    session = db_helper.get_scoped_session()
    query = select(Submenu)
    result = await session.execute(query)
    submenus = result.all()
    await session.close()
    return submenus


@pytest.fixture
async def post_submenu() -> dict[str, str]:
    return {
        "title": "submenu1",
        "description": "submenu1submenu1submenu1submenu1",
    }


@pytest.fixture
async def test_add_two_submenus(test_add_and_get_one_menu):
    menu = test_add_and_get_one_menu[0][0]
    submenus = [
        {
            "title": "SUBMENU1",
            "description": "SUBMENU1SUBMENU1SUBMENU1",
            "menu_id": menu.id,
        },
        {
            "title": "SUBMENU2",
            "description": "SUBMENU2SUBMENU2SUBMENU2",
            "menu_id": menu.id,
        },
    ]

    session = db_helper.get_scoped_session()
    for submenu in submenus:
        stmt = insert(Submenu).values(**submenu)
        await session.execute(stmt)
        await session.commit()


@pytest.fixture
async def test_add_and_get_one_submenu(test_add_and_get_one_menu):
    menu = test_add_and_get_one_menu[0][0]

    session = db_helper.get_scoped_session()

    stmt = insert(Submenu).values(
        title="SUBMENU1",
        description="SUBMENU1SUBMENU1SUBMENU1",
        menu_id=menu.id,
    )
    await session.execute(stmt)
    await session.commit()

    query = select(Submenu)
    result = await session.execute(query)
    submenus = result.all()
    await session.close()
    return submenus


@pytest.fixture
async def update_submenu() -> dict[str, str]:
    return {
        "title": "NEW SUBMENU",
        "description": "NEW SUBMENUNEW SUBMENUNEW SUBMENUNEW SUBMENU",
    }
