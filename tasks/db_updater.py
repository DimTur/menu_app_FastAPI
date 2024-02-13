from typing import Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Dish, Menu, Submenu


class DatabaseUpdater:
    """Добавление в БД данных из excel файла"""

    def __init__(
        self,
        parser_data: list[dict],
        session: AsyncSession,
    ):
        self.parser_data = parser_data
        self.session = session

    async def add_menu_items(self, full_base: list[dict]) -> None:
        for menu in full_base:
            existing_menu = await self.get_existing_menu(menu["id"])
            if existing_menu:
                await self.update_menu(existing_menu, menu)
            else:
                await self.add_new_menu(menu)

        await self.remove_menu_if_not_in_data(full_base)
        await self.session.commit()

    async def get_existing_menu(self, menu_id: int) -> Menu:
        existing_menu_query = select(Menu).filter_by(id=menu_id)
        result = await self.session.execute(existing_menu_query)
        return result.scalar()

    async def update_menu(self, existing_menu: Menu, new_menu_data: dict) -> None:
        existing_menu.title = new_menu_data["title"]
        existing_menu.description = new_menu_data["description"]

        for submenu in new_menu_data["submenus"]:
            existing_submenu = await self.get_existing_submenu(submenu["id"])
            if existing_submenu:
                await self.update_submenu(existing_submenu, submenu, existing_menu)
            else:
                await self.add_new_submenu(submenu, existing_menu)

        await self.remove_submenu_if_not_in_data(
            existing_menu, new_menu_data["submenus"]
        )

    async def get_existing_submenu(self, submenu_id: int) -> Submenu:
        existing_submenu_query = select(Submenu).filter_by(id=submenu_id)
        result = await self.session.execute(existing_submenu_query)
        return result.scalar()

    async def update_submenu(
        self, existing_submenu: Submenu, new_submenu_data: dict, menu: Menu
    ) -> None:
        existing_submenu.title = new_submenu_data["title"]
        existing_submenu.description = new_submenu_data["description"]

        for dish in new_submenu_data["dishes"]:
            existing_dish = await self.get_existing_dish(dish["id"])
            if existing_dish:
                await self.update_dish(existing_dish, dish, existing_submenu)
            else:
                await self.add_new_dish(dish, existing_submenu)

        await self.remove_dish_if_not_in_data(
            existing_submenu, new_submenu_data["dishes"]
        )

    async def get_existing_dish(self, dish_id: int) -> Dish:
        existing_dish_query = select(Dish).filter_by(id=dish_id)
        result = await self.session.execute(existing_dish_query)
        return result.scalar()

    async def update_dish(
        self, existing_dish: Dish, new_dish_data: dict, submenu: Submenu
    ) -> None:
        existing_dish.title = new_dish_data["title"]
        existing_dish.description = new_dish_data["description"]
        existing_dish.price = new_dish_data["price"]

    async def add_new_menu(self, menu_data: dict) -> None:
        menu_item = Menu(
            title=menu_data["title"],
            description=menu_data["description"],
            id=menu_data["id"],
            submenus=[],
        )
        self.session.add(menu_item)

        for submenu in menu_data["submenus"]:
            await self.add_new_submenu(submenu, menu_item)

    async def add_new_submenu(self, submenu_data: dict, menu: Menu) -> None:
        submenu_item = Submenu(
            title=submenu_data["title"],
            description=submenu_data["description"],
            id=submenu_data["id"],
            dishes=[],
        )
        menu.submenus.append(submenu_item)

        for dish in submenu_data["dishes"]:
            await self.add_new_dish(dish, submenu_item)

    async def add_new_dish(self, dish_data: dict, submenu: Submenu) -> None:
        dish_item = Dish(
            title=dish_data["title"],
            description=dish_data["description"],
            price=dish_data["price"],
            id=dish_data["id"],
        )
        submenu.dishes.append(dish_item)

    async def remove_menu_if_not_in_data(self, full_base: list[dict]) -> None:
        menu_ids_from_data = [menu["id"] for menu in full_base]
        menus_to_remove_query = select(Menu).filter(~Menu.id.in_(menu_ids_from_data))
        result = await self.session.execute(menus_to_remove_query)
        menus_to_remove = result.scalars().all()

        for menu in menus_to_remove:
            self.session.delete(menu)

    async def remove_submenu_if_not_in_data(
        self, menu: Menu, submenus_data: list[dict]
    ) -> None:
        submenu_ids_from_data = [submenu["id"] for submenu in submenus_data]
        submenus_to_remove_query = select(Submenu).filter(
            (Submenu.menu_id == menu.id) & (~Submenu.id.in_(submenu_ids_from_data))
        )
        result = await self.session.execute(submenus_to_remove_query)
        submenus_to_remove = result.scalars().all()

        for submenu in submenus_to_remove:
            self.session.delete(submenu)

    async def remove_dish_if_not_in_data(
        self, submenu: Submenu, dishes_data: list[dict]
    ) -> None:
        dish_ids_from_data = [dish["id"] for dish in dishes_data]
        dishes_to_remove_query = select(Dish).filter(
            (Dish.submenu_id == submenu.id) & (~Dish.id.in_(dish_ids_from_data))
        )
        result = await self.session.execute(dishes_to_remove_query)
        dishes_to_remove = result.scalars().all()

        for dish in dishes_to_remove:
            self.session.delete(dish)
