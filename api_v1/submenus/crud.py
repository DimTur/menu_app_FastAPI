import uuid

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import Submenu, Menu


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
