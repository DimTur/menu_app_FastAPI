import uuid
from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from core.redis.cache_repository import CacheRepository
from core.models import db_helper
from . import crud
from .schemas import Dish, DishCreate, DishUpdatePartial


class SubmenuService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_dishes(self) -> list[Dish] | None:
        """Возвращает список всех блюд для подменю"""
        pass

    async def create_dish(self) -> Dish:
        """Создание нового блюда"""
        pass

    async def get_dish_by_id(self) -> Dish:
        """Возвращает блюдо по его id"""
        pass

    async def update_dish(self) -> Dish:
        """Обдновляет блюдо по его id"""
        pass

    async def delete_dish(self) -> None:
        """Удаляет блюдо по его id"""
        pass
