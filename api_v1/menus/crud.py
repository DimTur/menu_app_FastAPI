import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import Menu, Submenu

from .schemas import MenuCreate, MenuUpdatePartial


async def get_all_base(session: AsyncSession):
    stmt = (
        select(Menu)
        .options(selectinload(Menu.submenus).selectinload(Submenu.dishes))
        .order_by(Menu.title)
    )
    result: Result = await session.execute(stmt)
    menus = result.scalars().fetchall()
    return list(menus)


async def get_menus(session: AsyncSession) -> list[Menu]:
    stmt = (
        select(Menu)
        .options(selectinload(Menu.submenus).selectinload(Submenu.dishes))
        .order_by(Menu.title)
    )
    result: Result = await session.execute(stmt)
    menus = result.scalars().all()

    for menu in menus:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)

    return list(menus)


async def get_menu_by_id(session: AsyncSession, menu_id: uuid.UUID) -> Menu | None:
    stmt = (
        select(Menu)
        .filter(Menu.id == menu_id)
        .options(selectinload(Menu.submenus).selectinload(Submenu.dishes))
    )
    result: Result = await session.execute(stmt)
    menu = result.scalar()

    if menu:
        menu.submenus_count = len(menu.submenus)
        menu.dishes_count = sum(len(submenu.dishes) for submenu in menu.submenus)

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
    menu_update: MenuUpdatePartial,
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
