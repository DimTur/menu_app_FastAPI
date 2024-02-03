import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Dish, db_helper

from . import crud
from .service_repository import DishService


async def dish_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    dish_id: Annotated[uuid.UUID, Path],
    repo: DishService = Depends(),
) -> Dish:
    dish = await repo.get_dish_by_id(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
    if dish is not None:
        return dish


async def dish_by_id_not_from_cache(
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
