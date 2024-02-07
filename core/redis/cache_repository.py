import pickle
import uuid

from fastapi import Depends

from core.models import Dish, Menu, Submenu
from core.redis.redis_helper import cache


class CacheRepository:
    def __init__(self, cacher=Depends(cache)) -> None:
        self.cacher = cacher

    async def clear_cache_by_mask(self, pattern: str) -> None:
        """Чистит кэш по шаблону"""
        for key in await self.cacher.keys(pattern + "*"):
            await self.cacher.delete(key)

    async def set_list_menus_cache(self, menus: list[Menu]) -> None:
        """Запись всех меню в кэш"""
        await self.cacher.set("/menus/", pickle.dumps(menus))

    async def get_list_menus_cache(self) -> list[Menu] | None:
        """Получение всех меню из кэша"""
        if (cached_menus := await self.cacher.get("/menus/")) is not None:
            return pickle.loads(cached_menus)
        return None

    async def create_menu_cache(self, menu: Menu) -> None:
        """Работа с кэшем при создании меню"""
        await self.delete_all_menus_from_cache()
        await self.cacher.set(f"/menus/{menu.id}/", pickle.dumps(menu))
        await self.delete_all_base_cache()

    async def update_menu_cache(self, menu: Menu) -> None:
        """Работа с кэшем при обновлении меню"""
        await self.delete_all_menus_from_cache()
        await self.cacher.set(f"/menus/{menu.id}/", pickle.dumps(menu))
        await self.delete_all_base_cache()

    async def set_menu_to_cache(self, menu: Menu) -> None:
        """Запись меню в кеш"""
        await self.cacher.set(f"/menus/{menu.id}/", pickle.dumps(menu))

    async def get_menu_from_cache(self, menu_id: uuid.UUID) -> Menu | None:
        """Получение меню по id из кэша"""
        if (cached_menu := await self.cacher.get(f"/menus/{menu_id}/")) is not None:
            return pickle.loads(cached_menu)
        return None

    async def delete_all_menus_from_cache(self) -> None:
        """Удаление всех меню из кэша"""
        await self.clear_cache_by_mask("/menus/")

    async def delete_menu_from_cache(self, menu_id: uuid.UUID) -> None:
        """Работа с кэшем при удалении меню"""
        await self.clear_cache_by_mask(f"/menus/{menu_id}/")
        await self.delete_all_menus_from_cache()
        await self.delete_all_base_cache()

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
        await self.clear_cache_by_mask(f"/menus/{menu_id}/")
        await self.delete_all_menus_from_cache()
        await self.set_submenu_to_cache(menu_id=menu_id, submenu=submenu)
        await self.delete_all_base_cache()

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
    ) -> Submenu | None:
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
        await self.delete_all_base_cache()

    async def delete_all_submenus_from_cache(self, menu_id: uuid.UUID) -> None:
        """Удаление всех подменю из кэша"""
        await self.cacher.delete(f"/menus/{menu_id}/submenus/")
        await self.delete_all_base_cache()

    async def delete_submenu_from_cache(self, submenu: Submenu) -> None:
        """Работа с кэшем при удалении подменю"""
        await self.clear_cache_by_mask(f"/menus/{submenu.menu_id}/")
        await self.delete_all_menus_from_cache()
        await self.delete_all_base_cache()

    async def set_list_dishes_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dishes: list[Dish],
    ) -> None:
        """Запись всех блюд в кэш"""
        await self.cacher.set(
            f"/menus/{menu_id}/submenus/{submenu_id}/dishes/",
            pickle.dumps(dishes),
        )

    async def get_list_dishes_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> list[Dish] | None:
        """Получение всех блюд из кэша"""
        if (
            cached_dishes := await self.cacher.get(
                f"/menus/{menu_id}/submenus/{submenu_id}/dishes/"
            )
        ) is not None:
            return pickle.loads(cached_dishes)
        return None

    async def create_dish_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: Dish,
    ) -> None:
        """Работа с кэшем при создании нового блюда"""
        await self.delete_all_menus_from_cache()
        await self.clear_cache_by_mask(f"/menus/{menu_id}/")
        await self.set_dish_to_cache(menu_id=menu_id, submenu_id=submenu_id, dish=dish)
        await self.delete_all_base_cache()

    async def set_dish_to_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: Dish,
    ) -> None:
        """Запись блюда в кеш"""
        await self.cacher.set(
            f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish.id}/",
            pickle.dumps(dish),
        )

    async def get_dish_from_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
    ) -> Dish | None:
        """Получение подменю по id из кэша"""
        if (
            cached_dish := await self.cacher.get(
                f"/menus/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}/"
            )
        ) is not None:
            return pickle.loads(cached_dish)
        return None

    async def update_dish_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: Dish,
    ) -> None:
        """Работа с кэшем при обновлении блюда"""
        await self.delete_all_menus_from_cache()
        await self.clear_cache_by_mask(f"/menus/{menu_id}/")
        await self.set_dish_to_cache(menu_id=menu_id, submenu_id=submenu_id, dish=dish)
        await self.delete_all_base_cache()

    async def delete_all_dishes_from_cache(
        self,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> None:
        """Удаление всех блюд из кэша"""
        await self.cacher.delete(f"/menus/{menu_id}/submenus/{submenu_id}/dishes/")
        await self.delete_all_base_cache()

    async def delete_dish_from_cache(self, menu_id: uuid.UUID) -> None:
        """Работа с кэшем при удалении блюда"""
        await self.clear_cache_by_mask(f"/menu/{menu_id}/")
        await self.delete_all_menus_from_cache()
        await self.delete_all_base_cache()

    async def set_all_base_cache(self, menus: list[Menu]) -> None:
        """Запись всех меню в кэш с подменю и блюдами"""
        await self.cacher.set("/menus/all/", pickle.dumps(menus))

    async def get_all_base_cache(self) -> list[Menu] | None:
        """Получение всейх меню из кэша с подменю и блюдами"""
        if (cached_menus_all := await self.cacher.get("/menus/all/")) is not None:
            return pickle.loads(cached_menus_all)
        return None

    async def delete_all_base_cache(self) -> None:
        """Удаление всех меню из кэша с подменю и блюдами"""
        await self.clear_cache_by_mask("/menus/all/")
