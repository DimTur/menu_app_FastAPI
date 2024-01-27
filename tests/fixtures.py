from typing import Any

import pytest

from api_v1.menus.schemas import MenuBase


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


@pytest.fixture(scope="module")
def saved_data() -> dict[str, Any]:
    return {}
