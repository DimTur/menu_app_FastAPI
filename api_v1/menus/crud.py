import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Menu

from .schemas import MenuCreate, MenuUpdate, MenuUpdatePartial


async def get_menus(session: AsyncSession) -> list[Menu]:
    stmt = select(Menu).order_by(Menu.title)
    result: Result = await session.execute(stmt)
    menus = result.scalars().all()
    return list(menus)


async def get_menu_by_id(session: AsyncSession, menu_id: uuid.UUID) -> Menu | None:
    return await session.get(Menu, menu_id)


async def create_menu(session: AsyncSession, menu_in: MenuCreate) -> Menu:
    menu = Menu(**menu_in.model_dump())
    session.add(menu)
    await session.commit()
    await session.refresh(menu)
    return menu


async def update_menu(
        session: AsyncSession,
        menu: Menu,
        menu_update: MenuUpdate | MenuUpdatePartial,
        partial: bool = False,
) -> Menu:
    for title, value in menu_update.model_dump(exclude_unset=partial).items():
        setattr(menu, title, value)
    await session.commit()
    return menu


async def delete_menu(
        session: AsyncSession,
        menu: Menu,
) -> None:
    await session.delete(menu)
    await session.commit()
