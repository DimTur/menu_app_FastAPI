import pickle

from fastapi import Depends

from core.models import Menu
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

    async def create_update_menu_cache(self, menu: Menu) -> None:
        """Работа с кэшем при создании нового меню"""
        await self.delete_all_menus_from_cache()
        await self.cacher.set(f"menu_{menu.id}", pickle.dumps(menu))

    async def set_menu_to_cache(self, menu: Menu) -> None:
        """Запись меню в кеш"""
        await self.cacher.set(f"menu_{menu.id}", pickle.dumps(menu))

    async def get_menu_from_cache(self, menu_id: Menu.id) -> Menu | None:
        """Получение меню по id из кэша"""
        if (cached_menu := await self.cacher.get(f"menu_{menu_id}")) is not None:
            return pickle.loads(cached_menu)
        return None

    async def delete_all_menus_from_cache(self) -> None:
        """Удаление всех меню из кэша"""
        await self.cacher.delete("menus")
