from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menus.cache import CacheRepository
from core.models import Menu, db_helper
from . import crud
from .schemas import MenuCreate


class MenuService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_menus(self) -> list[Menu]:
        """Получения списка меню"""
        cached_menus = await self.cache_repo.get_list_menus_cache()
        if cached_menus:
            return cached_menus
        menus = await crud.get_menus(session=self.session)
        await self.cache_repo.set_list_menus_cache(menus)
        return menus

    async def create_menu(self, menu_in: MenuCreate) -> Menu:
        """ "Создание нового меню"""
        menu = await crud.create_menu(session=self.session, menu_in=menu_in)
        await self.cache_repo.create_update_menu_cache(menu)
        return menu
