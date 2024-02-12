import uuid

from fastapi import BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.redis.cache_repository import CacheRepository

from ..menus.dependencies import menu_by_id_not_from_cache
from ..submenus.dependencies import submenu_by_id_not_from_cache
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
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> list[Dish]:
        """Возвращает список всех блюд для подменю"""
        try:
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
            background_tasks.add_task(
                self.cache_repo.set_list_dishes_cache,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dishes=dishes,
            )
            return dishes
        except DatabaseError:
            raise HTTPException(
                status_code=500, detail="Internal server error occurred"
            )

    async def create_dish(
        self,
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_in: DishCreate,
    ) -> Dish:
        """Создание нового блюда"""
        try:
            await menu_by_id_not_from_cache(menu_id=menu_id, session=self.session)
            await submenu_by_id_not_from_cache(
                menu_id=menu_id,
                submenu_id=submenu_id,
                session=self.session,
            )
            dish = await crud.create_dish(
                session=self.session,
                submenu_id=submenu_id,
                dish_in=dish_in,
            )
            background_tasks.add_task(
                self.cache_repo.create_dish_cache,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish=dish,
            )
            return dish
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Dish with the same title already exists",
            )

    async def get_dish_by_id(
        self,
        background_tasks: BackgroundTasks,
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

            if dish and dish.id is not None:
                background_tasks.add_task(
                    self.cache_repo.set_dish_to_cache,
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish=dish,
                )
                return dish

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )
        except AttributeError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="dish not found",
            )

    async def update_dish(
        self,
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: Dish,
        dish_update: DishUpdatePartial,
    ) -> Dish:
        """Обдновляет блюдо по его id"""
        try:
            dish = await crud.update_dish(
                session=self.session,
                dish=dish,
                dish_update=dish_update,
                partial=True,
            )
            background_tasks.add_task(
                self.cache_repo.update_dish_cache,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish=dish,
            )
            return dish
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Dish with the same title already exists",
            )

    async def delete_dish(
        self,
        background_tasks: BackgroundTasks,
        menu_id: uuid.UUID,
        dish: Dish,
    ) -> None:
        """Удаляет блюдо по его id"""
        background_tasks.add_task(
            self.cache_repo.delete_dish_from_cache,
            menu_id=menu_id,
        )
        await crud.delete_dish(session=self.session, dish=dish)
