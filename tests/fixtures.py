from typing import Any

import pytest


@pytest.fixture
async def post_menu() -> dict[str, str]:
    return {
        "title": "menu1",
        "description": "1111111111111",
    }


@pytest.fixture
async def update_menu() -> dict[str, str]:
    return {
        "title": "NEW MENU",
        "description": "NEW NEW NEW NEW NEW",
    }


@pytest.fixture
async def post_submenu() -> dict[str, str]:
    return {
        "title": "submenu1",
        "description": "submenu1submenu1submenu1submenu1",
    }


@pytest.fixture
async def update_submenu() -> dict[str, str]:
    return {
        "title": "NEW SUBMENU",
        "description": "NEW SUBMENUNEW SUBMENUNEW SUBMENUNEW SUBMENU",
    }


@pytest.fixture
async def post_dish() -> dict[str, Any]:
    return {
        "title": "DISH1",
        "description": "DISH1 DISH1 DISH1 DISH1 DISH1",
        "price": 20.4,
    }


@pytest.fixture
async def post_second_dish() -> dict[str, str]:
    return {
        "title": "DISH2",
        "description": "DISH2 DISH2 DISH2 DISH2 DISH2",
        "price": 30.8,
    }


@pytest.fixture
async def update_dish() -> dict[str, Any]:
    return {
        "title": "NEW DISH",
        "description": "NEW DISH NEW DISH NEW DISH NEW DISH",
        "price": 40,
    }


@pytest.fixture(scope="module")
def saved_data() -> dict[str, Any]:
    return {}
