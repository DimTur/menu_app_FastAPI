import uuid
from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Submenu

from . import crud


async def submenu_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Submenu:
    submenu = await crud.get_submenu_by_id(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if submenu is not None:
        return submenu

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Menu {menu_id} not found!",
    )
