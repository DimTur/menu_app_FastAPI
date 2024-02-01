import uuid

from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)

from core.models import Menu

from .service_repository import MenuService


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
