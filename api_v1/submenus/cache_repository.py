import pickle

from fastapi import Depends

from core.models import Submenu, Menu
from core.redis.redis_helper import cache


class CacheRepository:
    def __init__(self, cacher: cache = Depends(cache)) -> None:
        self.cacher = cacher

    async def set_list_submenus_cache(
        self,
        menu_id: Menu.id,
        submenus: list[Submenu],
    ):
        """Запись всех подменю в кэш"""
        await self.cacher.set(
            f"/menus/{menu_id}/submenus/",
            pickle.dumps(submenus),
        )

    async def get_list_submenus_cache(
        self,
        menu_id: Menu.id,
    ) -> list[Submenu] | None:
        """Получение всех подменю из кэша"""
        if (
            cached_submenus := await self.cacher.get(f"/menus/{menu_id}/submenus/")
        ) is not None:
            return pickle.loads(cached_submenus)
        return None
