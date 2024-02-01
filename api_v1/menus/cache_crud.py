from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menus.cache import CacheRepository
from core.models import Menu, db_helper
from . import crud


class MenuService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_menus(self) -> list[Menu]:
        cached_menus = await self.cache_repo.get_list_menus_cache()
        if cached_menus:
            return cached_menus
        items = await crud.get_menus(session=self.session)
        await self.cache_repo.set_list_menus_cache(items)
        return items


# @router.get("/", response_model=list[Menu])
# async def get_menus(
#     redis_client: cache = Depends(cache),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     if (cached_menus := redis_client.get("menus")) is not None:
#         return pickle.loads(cached_menus)
#
#     menus = await crud.get_menus(session=session)
#     redis_client.set("menus", pickle.dumps(menus))
#     return menus
