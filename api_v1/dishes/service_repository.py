import uuid

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.redis.cache_repository import CacheRepository
from core.models import db_helper
from . import crud
from .schemas import Dish, DishCreate, DishUpdatePartial


class DishService:
    def __init__(
        self,
        cache_repo: CacheRepository = Depends(),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    ) -> None:
        self.session = session
        self.cache_repo = cache_repo

    async def get_all_dishes(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> list[Dish] | None:
        """Возвращает список всех блюд для подменю"""
        cached_dishes = await self.cache_repo.get_list_dishes_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if cached_dishes:
            return cached_dishes
        dishes = await crud.get_dishes(
            session=self.session,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        await self.cache_repo.set_list_dishes_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dishes=dishes,
        )
        return dishes

    async def create_dish(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_in: DishCreate,
    ) -> Dish:
        """Создание нового блюда"""
        dish = await crud.create_dish(
            session=self.session,
            submenu_id=submenu_id,
            dish_in=dish_in,
        )
        await self.cache_repo.create_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish=dish,
        )
        return dish

    async def get_dish_by_id(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
    ) -> Dish | None:
        """Возвращает блюдо по его id"""
        cached_dish = await self.cache_repo.get_dish_from_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        if cached_dish:
            return cached_dish

        try:
            dish = await crud.get_dish_by_id(
                session=self.session,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=dish_id,
            )

            if dish.id is not None:
                await self.cache_repo.set_dish_to_cache(
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish=dish,
                )
                return dish

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"dish not found",
            )
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

    async def update_dish(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: Dish,
        dish_update: DishUpdatePartial,
    ) -> Dish:
        """Обдновляет блюдо по его id"""
        dish = await crud.update_dish(
            session=self.session,
            dish=dish,
            dish_update=dish_update,
            partial=True,
        )
        await self.cache_repo.update_dish_cache(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish=dish,
        )
        return dish

    async def delete_dish(
        self,
        menu_id: uuid.UUID,
        dish: Dish,
    ) -> None:
        """Удаляет блюдо по его id"""
        await self.cache_repo.delete_dish_from_cache(menu_id=menu_id, dish=dish)
