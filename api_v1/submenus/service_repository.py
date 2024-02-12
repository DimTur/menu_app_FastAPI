import uuid

from fastapi import BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.redis.cache_repository import CacheRepository

from ..menus.dependencies import menu_by_id_not_from_cache
from . import crud
from .schemas import Submenu, SubmenuCreate, SubmenuUpdatePartial


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
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
    ) -> list[Submenu]:
        """Возвращает список всех подменю для блюда"""
        try:
            cached_submenus = await self.cache_repo.get_list_submenus_cache(menu_id)
            if cached_submenus:
                return cached_submenus
            submenus = await crud.get_submenus(session=self.session, menu_id=menu_id)
            background_tasks.add_task(
                self.cache_repo.set_list_submenus_cache,
                menu_id=menu_id,
                submenus=submenus,
            )
            return submenus
        except DatabaseError:
            raise HTTPException(
                status_code=500, detail="Internal server error occurred"
            )

    async def create_submenu(
        self,
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
        submenu_in: SubmenuCreate,
    ) -> Submenu:
        """Создание нового подменю"""
        try:
            await menu_by_id_not_from_cache(menu_id, session=self.session)
            submenu = await crud.create_submenu(
                session=self.session,
                menu_id=menu_id,
                submenu_in=submenu_in,
            )
            background_tasks.add_task(
                self.cache_repo.create_submenu_cache,
                menu_id=menu_id,
                submenu=submenu,
            )
            return submenu
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Submenu with the same title already exists",
            )

    async def get_submenu_by_id(
        self,
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> Submenu | None:
        """Возвращает подменю по его id"""
        cached_submenu = await self.cache_repo.get_submenu_from_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if cached_submenu:
            return cached_submenu
        try:
            submenu = await crud.get_submenu_by_id(
                session=self.session,
                menu_id=menu_id,
                submenu_id=submenu_id,
            )

            if submenu and submenu.id is not None:
                background_tasks.add_task(
                    self.cache_repo.set_submenu_to_cache,
                    menu_id=menu_id,
                    submenu=submenu,
                )
                return submenu

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="submenu not found",
            )

    async def update_submenu(
        self,
        background_tasks: BackgroundTasks,
        submenu: Submenu,
        submenu_update: SubmenuUpdatePartial,
    ) -> Submenu:
        """Обновляет подменю по его id"""
        try:
            submenu = await crud.update_submenu(
                session=self.session,
                submenu=submenu,
                submenu_update=submenu_update,
                partial=True,
            )
            background_tasks.add_task(
                self.cache_repo.update_submenu_cache,
                menu_id=submenu.menu_id,
                submenu=submenu,
            )
            return submenu
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Submenu with the same title already exists",
            )

    async def delete_submenu(
        self,
        background_tasks: BackgroundTasks,
        submenu: Submenu,
    ) -> None:
        """Удаляет подменю по его id"""
        background_tasks.add_task(
            self.cache_repo.delete_submenu_from_cache,
            submenu=submenu,
        )
        await crud.delete_submenu(session=self.session, submenu=submenu)
