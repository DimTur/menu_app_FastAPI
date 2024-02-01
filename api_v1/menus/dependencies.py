import uuid
import pickle
from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Menu
from core.redis import cache

from . import crud
from .cache_crud import MenuService


class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""


async def menu_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    repo: MenuService = Depends(),
) -> Menu:
    menu = await repo.get_menu_by_id(menu_id=menu_id)
    if menu is not None:
        return menu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"menu not found",
    )
