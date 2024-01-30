import pickle

from redis import Redis
from fastapi import Depends

from core.models import Menu
from core.redis.redis_helper import cache


class CacheRepository:
    def __init__(self, cacher: cache = Depends(cache)) -> None:
        self.cacher = cacher

    async def set_list_menus_cache(self, items: list[Menu]) -> None:
        """Запись всех меню в кэш"""
        await self.cacher.set("list_menus", pickle.dumps(items))

    # menus = await crud.get_menus(session=session)
    # redis_client.set("menus", pickle.dumps(menus))
    # return menus

    async def get_list_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кэша"""
        if (cached_menus := self.cacher.get("list_menus")) is not None:
            return pickle.loads(cached_menus)
        # cache = self.cacher.get("/")
        # if cache:
        #     items = pickle.loads(cache)
        #     return items
        return None
