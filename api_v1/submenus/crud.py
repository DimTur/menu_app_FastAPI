import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Submenu, Menu
from .schemas import SubmenuCreate, SubmenuUpdate, SubmenuUpdatePartial


async def get_submenus(session: AsyncSession, menu_id: uuid.UUID) -> list[Submenu]:
    stmt = (
        select(Submenu)
        .join(Submenu.menu)
        .options(joinedload(Submenu.menu))
        .where(Menu.id == menu_id)
        .order_by(Submenu.title)
    )
    result: Result = await session.execute(stmt)
    submenus = result.scalars().all()
    return list(submenus)


async def get_submenu_by_id(
    session: AsyncSession,
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
) -> Submenu | None:
    stmt = (
        select(Submenu)
        .join(Submenu.menu)
        .options(joinedload(Submenu.menu))
        .where(Menu.id == menu_id)
        .where(submenu_id == submenu_id)
    )
    result: Result = await session.execute(stmt)
    submenu = result.scalar()
    return submenu


async def create_submenu(
    session: AsyncSession,
    menu_id: uuid.UUID,
    submenu_in: SubmenuCreate,
) -> Submenu:
    submenu = Submenu(menu_id=menu_id, **submenu_in.model_dump())
    session.add(submenu)
    await session.commit()
    await session.refresh(submenu)
    return submenu


async def update_submenu(
    session: AsyncSession,
    # menu_id: uuid.UUID,
    submenu: Submenu,
    submenu_update: SubmenuUpdate | SubmenuUpdatePartial,
    partial: bool = True,
) -> Submenu:
    # submenu = [Submenu(menu_id=menu_id)]
    for title, value in submenu_update.model_dump(exclude_unset=partial).items():
        setattr(submenu, title, value)
    await session.commit()
    return submenu
