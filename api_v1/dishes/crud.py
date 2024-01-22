import uuid

from sqlalchemy import select, or_, and_
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api_v1.dishes.schemas import DishCreate
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


# async def get_dishes(
#     session: AsyncSession,
#     menu_id: uuid.UUID,
#     submenu_id: uuid.UUID,
# ) -> list[Dish]:
#     submenu = (
#         select(Submenu)
#         .join(Submenu.menu)
#         .options(joinedload(Submenu.menu))
#         .where(Menu.id == menu_id)
#     )
#     stmt = (
#         select(Dish)
#         .join(Dish.submenu)
#         .options(joinedload(Dish.submenu))
#         .where(Submenu.id == submenu_id)
#         .order_by(Dish.title)
#     )
#     result: Result = await session.execute(stmt)
#     dishes = result.scalars().all()
#     return list(dishes)


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
    # menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_in: DishCreate,
) -> Dish:
    dish = Dish(submenu_id=submenu_id, **dish_in.model_dump())
    session.add(dish)
    await session.commit()
    await session.refresh(dish)
    return dish


async def update_dish():
    pass


async def delete_dish():
    pass
