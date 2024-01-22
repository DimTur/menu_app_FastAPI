import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Dish, Submenu, Menu


async def get_dishes(
    session: AsyncSession,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
) -> list[Dish]:
    stmt = (
        select(Dish)
        .join(Dish.submenu)
        .join(Submenu.menu)
        .options(joinedload(Dish.submenu).joinedload(Submenu.menu))
        .where(Submenu.id == submenu_id)
        .where(Menu.id == menu_id)
        .order_by(Dish.title)
    )
    result: Result = await session.execute(stmt)
    dishes = result.scalars().all()
    return list(dishes)


async def get_dish_by_id():
    pass


async def create_dish():
    pass


async def update_dish():
    pass


async def delete_dish():
    pass
