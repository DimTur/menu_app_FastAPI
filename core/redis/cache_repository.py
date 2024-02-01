import pickle
import uuid

from fastapi import Depends

from core.models import Menu, Submenu
from core.redis.redis_helper import cache


class CacheRepository:
    def __init__(self, cacher: cache = Depends(cache)) -> None:
        self.cacher = cacher

    async def set_list_menus_cache(self, menus: list[Menu]) -> None:
        """Запись всех меню в кэш"""
        await self.cacher.set("menus", pickle.dumps(menus))

    async def get_list_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кэша"""
        if (cached_menus := await self.cacher.get("menus")) is not None:
            return pickle.loads(cached_menus)
        return None

    async def create_menu_cache(self, menu: Menu) -> None:
        """Работа с кэшем при создании меню"""
        await self.delete_all_menus_from_cache()
        await self.cacher.set(f"menu_{menu.id}", pickle.dumps(menu))

    async def update_menu_cache(self, menu: Menu) -> None:
        """Работа с кэшем при обновлении меню"""
        await self.delete_all_menus_from_cache()
        await self.delete_menu_from_cache(menu_id=menu.id)
        await self.cacher.set(f"menu_{menu.id}", pickle.dumps(menu))

    async def set_menu_to_cache(self, menu: Menu) -> None:
        """Запись меню в кеш"""
        await self.cacher.set(f"menu_{menu.id}", pickle.dumps(menu))

    async def get_menu_from_cache(self, menu_id: uuid.UUID) -> Menu | None:
        """Получение меню по id из кэша"""
        if (cached_menu := await self.cacher.get(f"menu_{menu_id}")) is not None:
            return pickle.loads(cached_menu)
        return None

    async def delete_all_menus_from_cache(self) -> None:
        """Удаление всех меню из кэша"""
        await self.cacher.delete("menus")

    async def delete_menu_from_cache(self, menu_id: uuid.UUID) -> None:
        """Работа с кэшем при удалении меню"""
        await self.cacher.delete(f"menu_{menu_id}")
        await self.delete_all_menus_from_cache()

    async def set_list_submenus_cache(
        self,
        menu_id: uuid.UUID,
        submenus: list[Submenu],
    ) -> None:
        """Запись всех подменю в кэш"""
        await self.cacher.set(
            f"/menus/{menu_id}/submenus/",
            pickle.dumps(submenus),
        )

    async def get_list_submenus_cache(
        self,
        menu_id: uuid.UUID,
    ) -> list[Submenu] | None:
        """Получение всех подменю из кэша"""
        if (
            cached_submenus := await self.cacher.get(f"/menus/{menu_id}/submenus/")
        ) is not None:
            return pickle.loads(cached_submenus)
        return None

    async def create_submenu_cache(
        self,
        menu_id: uuid.UUID,
        submenu: Submenu,
    ) -> None:
        """Работа с кэшем при создании нового подменю"""
        await self.delete_all_submenus_from_cache(menu_id=menu_id)
        await self.delete_menu_from_cache(menu_id=menu_id)
        await self.set_submenu_to_cache(menu_id=menu_id, submenu=submenu)

    async def set_submenu_to_cache(
        self,
        menu_id: uuid.UUID,
        submenu: Submenu,
    ) -> None:
        """Запись подменю в кеш"""
        await self.cacher.set(
            f"/menus/{menu_id}/submenus/{submenu.id}/", pickle.dumps(submenu)
        )

    async def get_submenu_from_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> Menu | None:
        """Получение подменю по id из кэша"""
        if (
            cached_submenu := await self.cacher.get(
                f"/menus/{menu_id}/submenus/{submenu_id}/"
            )
        ) is not None:
            return pickle.loads(cached_submenu)
        return None

    async def update_submenu_cache(
        self,
        menu_id: uuid.UUID,
        submenu: Submenu,
    ) -> None:
        """Работа с кэшем при обновлении подменю"""
        await self.delete_all_submenus_from_cache(submenu.menu_id)
        await self.delete_all_menus_from_cache()
        await self.set_submenu_to_cache(submenu=submenu, menu_id=menu_id)

    async def delete_all_submenus_from_cache(self, menu_id: uuid.UUID) -> None:
        """Удаление всех подменю из кэша"""
        await self.cacher.delete(f"/menus/{menu_id}/submenus/")

    async def delete_submenu_from_cache(self, submenu: Submenu) -> None:
        """Работа с кэшем при удалении подменю"""
        await self.cacher.delete(f"menu_{submenu.menu_id}")
        await self.delete_all_submenus_from_cache(submenu.menu_id)
        await self.delete_menu_from_cache(menu_id=submenu.menu_id)
        await self.delete_all_menus_from_cache()
