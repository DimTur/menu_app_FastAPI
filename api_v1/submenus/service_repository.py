import uuid
from typing import Annotated, List

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.submenus.cache_repository import CacheRepository
from core.models import Submenu, Menu, db_helper
from . import crud
from .schemas import SubmenuCreate, SubmenuUpdatePartial


class SubmenuService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_submenus(
        self,
        menu_id: Annotated[uuid.UUID, Path],
    ) -> list[Submenu]:
        """Получения списка подменю"""
        cached_menus = await self.cache_repo.get_list_submenus_cache(menu_id)
        if cached_menus:
            return cached_menus
        submenus = await crud.get_submenus(session=self.session, menu_id=menu_id)
        await self.cache_repo.set_list_submenus_cache(
            menu_id=menu_id, submenus=submenus
        )
        return submenus
