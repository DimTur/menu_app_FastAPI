import uuid

from fastapi import BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Menu, db_helper
from core.redis.cache_repository import CacheRepository

from . import crud
from .schemas import FullBase, MenuCreate, MenuUpdatePartial


class MenuService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_base(
        self,
        background_tasks: BackgroundTasks,
    ) -> list[FullBase]:
        """Получение списка всех меню с подменю и блюдами"""
        try:
            cached_all_base = await self.cache_repo.get_all_base_cache()
            if cached_all_base:
                return cached_all_base
            all_base = await crud.get_all_base(session=self.session)
            background_tasks.add_task(self.cache_repo.set_all_base_cache, all_base)
            return all_base
        except DatabaseError:
            raise HTTPException(
                status_code=500, detail="Internal server error occurred"
            )

    async def get_all_menus(
        self,
        background_tasks: BackgroundTasks,
    ) -> list[Menu]:
        """Получения списка меню"""
        try:
            cached_menus = await self.cache_repo.get_list_menus_cache()
            if cached_menus:
                return cached_menus
            menus = await crud.get_menus(session=self.session)
            background_tasks.add_task(self.cache_repo.set_list_menus_cache, menus)
            # await self.cache_repo.set_list_menus_cache(menus)
            return menus
        except DatabaseError:
            raise HTTPException(
                status_code=500, detail="Internal server error occurred"
            )

    async def create_menu(
        self,
        background_tasks: BackgroundTasks,
        menu_in: MenuCreate,
    ) -> Menu:
        """Создание нового меню"""
        try:
            menu = await crud.create_menu(session=self.session, menu_in=menu_in)
            background_tasks.add_task(self.cache_repo.create_menu_cache, menu)
            # await self.cache_repo.create_menu_cache(menu)
            return menu
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Menu with the same title already exists",
            )

    async def get_menu_by_id(
        self,
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
    ) -> Menu | None:
        """Получение меню по id"""
        cached_menu = await self.cache_repo.get_menu_from_cache(menu_id=menu_id)
        if cached_menu:
            return cached_menu

        menu = await crud.get_menu_by_id(session=self.session, menu_id=menu_id)
        if menu and menu.id:
            background_tasks.add_task(self.cache_repo.set_menu_to_cache, menu)
            # await self.cache_repo.set_menu_to_cache(menu=menu)
            return menu

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="menu not found",
        )

    async def update_menu(
        self,
        background_tasks: BackgroundTasks,
        menu: Menu,
        menu_update: MenuUpdatePartial,
    ) -> Menu:
        """Обновление меню"""
        try:
            updated_menu = await crud.update_menu(
                session=self.session,
                menu=menu,
                menu_update=menu_update,
                partial=True,
            )
            background_tasks.add_task(self.cache_repo.update_menu_cache, updated_menu)
            # await self.cache_repo.update_menu_cache(updated_menu)
            return updated_menu
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Menu with the same title already exists",
            )

    async def delete_menu(
        self,
        background_tasks: BackgroundTasks,
        menu: Menu,
    ) -> None:
        """Удаление меню по id"""
        background_tasks.add_task(self.cache_repo.delete_menu_from_cache, menu.id)
        # await self.cache_repo.delete_menu_from_cache(menu_id=menu.id)
        await crud.delete_menu(session=self.session, menu=menu)
