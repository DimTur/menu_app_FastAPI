import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.redis.cache_repository import CacheRepository

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
        menu_id: uuid.UUID,
    ) -> list[Submenu]:
        """Возвращает список всех подменю для блюда"""
        cached_submenus = await self.cache_repo.get_list_submenus_cache(menu_id)
        if cached_submenus:
            return cached_submenus
        submenus = await crud.get_submenus(session=self.session, menu_id=menu_id)
        await self.cache_repo.set_list_submenus_cache(
            menu_id=menu_id,
            submenus=submenus,
        )
        return submenus

    async def create_submenu(
        self,
        menu_id: uuid.UUID,
        submenu_in: SubmenuCreate,
    ) -> Submenu:
        """Создание нового подменю"""
        submenu = await crud.create_submenu(
            session=self.session,
            menu_id=menu_id,
            submenu_in=submenu_in,
        )
        await self.cache_repo.create_submenu_cache(menu_id=menu_id, submenu=submenu)
        return submenu

    async def get_submenu_by_id(
        self,
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

            if submenu.id is not None:
                await self.cache_repo.set_submenu_to_cache(
                    menu_id=menu_id, submenu=submenu
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
        submenu: Submenu,
        submenu_update: SubmenuUpdatePartial,
    ) -> Submenu:
        """Обновляет подменю по его id"""
        submenu = await crud.update_submenu(
            session=self.session,
            submenu=submenu,
            submenu_update=submenu_update,
            partial=True,
        )
        await self.cache_repo.update_submenu_cache(
            menu_id=submenu.menu_id,
            submenu=submenu,
        )
        return submenu

    async def delete_submenu(self, submenu: Submenu) -> None:
        """Удаляет подменю по его id"""
        await self.cache_repo.delete_submenu_from_cache(submenu=submenu)
        await crud.delete_submenu(session=self.session, submenu=submenu)
