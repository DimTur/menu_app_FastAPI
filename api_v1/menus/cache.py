import pickle

from fastapi import Depends

from core.models import Menu
from core.redis.redis_helper import cache


class CacheRepository:
    def __init__(self, cacher: cache = Depends(cache)) -> None:
        self.cacher = cacher

    async def set_list_menus_cache(self, items: list[Menu]) -> None:
        """Запись всех меню в кэш"""
        await self.cacher.set("menus", pickle.dumps(items))

    async def get_list_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кэша"""
        cached_menus = await self.cacher.get("menus")
        if cached_menus is not None:
            items = await pickle.loads(cached_menus)
            return items
        return None
        # if (cached_menus := await self.cacher.get("menus")) is not None:
        #     return pickle.loads(cached_menus)
        # return None
