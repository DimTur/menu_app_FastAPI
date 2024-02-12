import json

from sqlalchemy.exc import IntegrityError

from core.models import db_helper

from .parser import menu_json


class MenuLoader:
    def __init__(self, menu_json):
        self.menu_json = menu_json

    def load_menu_to_db(self):
        menu_data = json.loads(self.menu_json)
        with db_helper.connect() as connection:
            with connection.transaction():
                for menu in menu_data:
                    self._load_menu(connection, menu)

    def _load_menu(self, connection, menu):
        # Добавление меню
        try:
            connection.execute(
                "INSERT INTO menus (id, title, description) VALUES ($1, $2, $3)",
                menu["id"],
                menu["title"],
                menu["description"],
            )
        except IntegrityError:
            pass  # Если меню уже существует, пропускаем

        # Добавление подменю и блюд
        for submenu in menu["submenus"]:
            self._load_submenu(connection, menu["id"], submenu)

    def _load_submenu(self, connection, menu_id, submenu):
        # Добавление подменю
        try:
            connection.execute(
                "INSERT INTO submenus (id, title, description, menu_id) VALUES ($1, $2, $3, $4)",
                submenu["id"],
                submenu["title"],
                submenu["description"],
                menu_id,
            )
        except IntegrityError:
            pass  # Если подменю уже существует, пропускаем

        # Добавление блюд
        for dish in submenu["dishes"]:
            self._load_dish(connection, submenu["id"], dish)

    def _load_dish(self, connection, submenu_id, dish):
        # Добавление блюда
        try:
            connection.execute(
                "INSERT INTO dishes (id, title, description, price, submenu_id) VALUES ($1, $2, $3, $4, $5)",
                dish["id"],
                dish["title"],
                dish["description"],
                dish["price"],
                submenu_id,
            )
        except IntegrityError:
            pass  # Если блюдо уже существует, пропускаем


# Пример использования
menu_json = menu_json
menu_loader = MenuLoader(menu_json)
# await menu_loader.load_menu_to_db()
