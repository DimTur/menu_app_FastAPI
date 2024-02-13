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

    async def add_menu_items(self, full_base):
        for menu in full_base:
            menu_item = Menu(
                title=menu["title"],
                description=menu["description"],
                id=menu["id"],
                submenus=[],
            )

            for submenu in menu["submenus"]:
                submenu_item = Submenu(
                    title=submenu["title"],
                    description=submenu["description"],
                    id=submenu["id"],
                    dishes=[],
                )
                menu_item.submenus.append(submenu_item)

                for dish in submenu["dishes"]:
                    dish_item = Dish(
                        title=dish["title"],
                        description=dish["description"],
                        price=dish["price"],
                        id=dish["id"],
                    )
                    submenu_item.dishes.append(dish_item)

            self.session.add(menu_item)
            await self.session.commit()
            await self.session.refresh(menu_item)
