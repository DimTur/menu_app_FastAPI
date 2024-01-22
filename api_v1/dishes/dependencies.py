import uuid
from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Dish

from . import crud


async def dish_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    dish_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Dish:
    dish = await crud.get_dish_by_id(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
    if dish is not None:
        return dish

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"dish not found",
    )
