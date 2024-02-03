import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Menu, db_helper
from core.redis.cache_repository import CacheRepository

from . import crud
from .schemas import MenuCreate, MenuUpdatePartial


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
        """Создание нового меню"""
        menu = await crud.create_menu(session=self.session, menu_in=menu_in)
        await self.cache_repo.create_menu_cache(menu)
        return menu

    async def get_menu_by_id(self, menu_id: uuid.UUID) -> Menu | None:
        """Получение меню по id"""
        cached_menu = await self.cache_repo.get_menu_from_cache(menu_id=menu_id)
        if cached_menu:
            return cached_menu

        menu = await crud.get_menu_by_id(session=self.session, menu_id=menu_id)
        if menu and menu.id:
            await self.cache_repo.set_menu_to_cache(menu=menu)
            return menu

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )

    async def update_menu(
        self,
        menu: Menu,
        menu_update: MenuUpdatePartial,
    ) -> Menu:
        """Обновление меню"""
        updated_menu = await crud.update_menu(
            session=self.session,
            menu=menu,
            menu_update=menu_update,
            partial=True,
        )
        await self.cache_repo.update_menu_cache(updated_menu)
        return updated_menu

    async def delete_menu(self, menu: Menu) -> None:
        """Удаление меню по id"""
        await self.cache_repo.delete_menu_from_cache(menu_id=menu.id)
        await crud.delete_menu(session=self.session, menu=menu)
