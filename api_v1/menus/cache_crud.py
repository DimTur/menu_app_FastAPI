from fastapi import Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.menus.cache import CacheRepository
from core.models import Menu, db_helper
from .crud import get_menus


class MenuService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_menus(self, background_tasks: BackgroundTasks) -> list[Menu]:
        cache = await self.cache_repo.get_list_menus_cache()
        if cache:
            return cache
        items = await get_menus(session=self.session)
        background_tasks.add_task(self.cache_repo.set_list_menus_cache, items)
        return items
