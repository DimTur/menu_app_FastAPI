import uuid

from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Menu, db_helper
from .crud import get_menu_by_id

from .service_repository import MenuService


async def menu_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    repo: MenuService = Depends(),
) -> Menu:
    menu = await repo.get_menu_by_id(menu_id=menu_id)
    if menu is not None:
        return menu


async def menu_by_id_not_from_cache(
    menu_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Menu:
    menu = await get_menu_by_id(session=session, menu_id=menu_id)
    if menu is not None:
        return menu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"menu not found",
    )
