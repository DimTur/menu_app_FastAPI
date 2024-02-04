import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Submenu, db_helper

from .crud import get_submenu_by_id
from .service_repository import SubmenuService


async def submenu_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    repo: SubmenuService = Depends(),
) -> Submenu:
    submenu = await repo.get_submenu_by_id(menu_id=menu_id, submenu_id=submenu_id)
    if submenu is not None:
        return submenu
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="submenu not found",
        )


async def submenu_by_id_not_from_cache(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Submenu:
    menu = await get_submenu_by_id(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if menu is not None:
        return menu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="submenu not found",
    )
