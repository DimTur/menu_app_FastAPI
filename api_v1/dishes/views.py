import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

from .dependencies import dish_by_id
from ..submenus.dependencies import submenu_by_id
from ..submenus.schemas import Submenu

router = APIRouter(tags=["Dishes"])

from . import crud
from .schemas import Dish, DishCreate, DishUpdatePartial


@router.get("/", response_model=list[Dish])
async def get_dishes(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_dishes(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@router.post(
    "/",
    response_model=Dish,
    status_code=status.HTTP_201_CREATED,
)
async def create_dish(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    dish_in: DishCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    dish_in_data = dish_in.model_dump()
    dish_in_data["price"] = str(dish_in_data["price"])

    return await crud.create_dish(
        session=session,
        # menu_id=menu_id,
        submenu_id=submenu_id,
        dish_in=dish_in,
    )


@router.get("/{dish_id}", response_model=Dish)
async def get_dish_by_if(
    dish: Dish = Depends(dish_by_id),
):
    return dish


@router.patch("/{dish_id}")
async def update_dish_partial(
    dish_update: DishUpdatePartial,
    dish: Dish = Depends(dish_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_dish(
        session=session,
        dish=dish,
        dish_update=dish_update,
        partial=True,
    )


@router.delete("/{dish_id}")
async def delete_dish(
    dish: Dish = Depends(dish_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    await crud.delete_dish(
        session=session,
        dish=dish,
    )
