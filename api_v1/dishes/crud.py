import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api_v1.dishes.schemas import DishCreate, DishUpdate, DishUpdatePartial
from core.models import Dish, Submenu, Menu


async def get_dishes(
    session: AsyncSession,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
) -> list[Dish]:
    stmt = (
        select(Dish)
        .join(Dish.submenu)
        .options(joinedload(Dish.submenu))
        .where(Submenu.id == submenu_id and Menu.id == menu_id)
    )
    result: Result = await session.execute(stmt)
    dishes = result.scalars().all()
    return list(dishes)


async def get_dish_by_id(
    session: AsyncSession,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
) -> Dish | None:
    stmt = (
        select(Dish)
        .join(Dish.submenu)
        .join(Submenu.menu)
        .options(joinedload(Dish.submenu).joinedload(Submenu.menu))
        .where(Menu.id == menu_id)
        .where(Submenu.id == submenu_id)
        .where(Dish.id == dish_id)
    )
    result: Result = await session.execute(stmt)
    submenu = result.scalar()
    return submenu


async def create_dish(
    session: AsyncSession,
    submenu_id: uuid.UUID,
    dish_in: DishCreate,
) -> Dish:
    dish = Dish(submenu_id=submenu_id, **dish_in.model_dump())
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    return dish


async def update_dish(
    session: AsyncSession,
    dish: Dish,
    dish_update: DishUpdate | DishUpdatePartial,
    partial: bool = True,
) -> Dish:
    for title, value in dish_update.model_dump(exclude_unset=partial).items():
        setattr(dish, title, value)

    if "price" in dish_update:
        dish.price = str(dish.price)

    await session.commit()
    dish.price = str(dish.price)
    return dish


async def delete_dish(
    session: AsyncSession,
    dish: Dish,
) -> None:
    await session.delete(dish)
    await session.commit()
