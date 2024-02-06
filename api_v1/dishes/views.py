import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from .dependencies import dish_by_id, dish_by_id_not_from_cache
from .schemas import Dish, DishCreate, DishUpdatePartial
from .service_repository import DishService

router = APIRouter(tags=["Dishes"])


@router.get(
    "/",
    response_model=list[Dish],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список всех блюд подменю",
)
async def get_dishes(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    repo: DishService = Depends(),
):
    return await repo.get_all_dishes(
        menu_id=menu_id,
        submenu_id=submenu_id,
    )


@router.post(
    "/",
    response_model=Dish,
    status_code=status.HTTP_201_CREATED,
    summary="Создает новое блюдо",
)
async def create_dish(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    dish_in: DishCreate,
    repo: DishService = Depends(),
):
    dish_in_data = dish_in.model_dump()
    dish_in_data["price"] = str(dish_in_data["price"])

    return await repo.create_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_in=dish_in,
    )


@router.get(
    "/{dish_id}",
    response_model=Dish,
    status_code=status.HTTP_200_OK,
    summary="Возвращает блюдо по его id",
)
async def get_dish_by_id(
    dish: Dish = Depends(dish_by_id),
):
    return dish


@router.patch(
    "/{dish_id}",
    response_model=Dish,
    status_code=status.HTTP_200_OK,
    summary="Обновляет блюдо по его id",
)
async def update_dish_partial(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    dish_update: DishUpdatePartial,
    dish: Dish = Depends(dish_by_id_not_from_cache),
    repo: DishService = Depends(),
):
    return await repo.update_dish(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish=dish,
        dish_update=dish_update,
    )


@router.delete(
    "/{dish_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаляет блюдо по его id",
)
async def delete_dish(
    menu_id: Annotated[uuid.UUID, Path],
    dish: Dish = Depends(dish_by_id),
    repo: DishService = Depends(),
) -> None:
    await repo.delete_dish(menu_id=menu_id, dish=dish)
