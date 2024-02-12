from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet

FILE_PATH = "/menu_app_FastApi/admin/Menu.xlsx"


class ParserService:
    """Класс для парсинга данных из файла и записи в список"""

    def __init__(self) -> None:
        self.sheet: Worksheet = load_workbook(filename=FILE_PATH).active
        self.result: list = []

    def get_dish(self, row: int) -> dict:
        """Извлекает данные о блюде и формирует словарь"""
        dish: dict[str, str | int] = {}
        cells = self.sheet[f"C{row}":f"G{row}"][0]  # type: ignore
        dish["id"] = cells[0].value
        dish["title"] = cells[1].value
        dish["description"] = cells[2].value
        dish["price"] = cells[3].value
        if cells[4]:
            dish["discount"] = cells[3].value
        else:
            dish["discount"] = 0
        return dish

    def get_submenu(self, row: int, max_row: int) -> dict:
        """Извлекает данные о подменю и формирует словарь"""
        submenu: dict = {"dishes": []}
        cells = self.sheet[f"C{row}":f"D{row}"][0]  # type: ignore
        submenu["id"] = cells[0].value
        submenu["title"] = cells[1].value
        submenu["description"] = cells[2].value
        for i in range(row + 1, max_row + 1):
            if self.sheet[f"C{i}"].value:
                dish = self.get_dish(i)
                if dish["description"]:
                    submenu["dishes"].append(dish)
                else:
                    break
        return submenu

    def get_menu(self, row: int, max_row: int) -> dict:
        """Извлекает данные о меню и формирует словарь"""
        menu: dict = {"submenus": []}
        cells = self.sheet[f"A{row}":f"C{row}"][0]   # type: ignore
        menu["id"] = cells[0].value
        menu["title"] = cells[1].value
        menu["description"] = cells[2].value
        for i in range(row + 1, max_row + 1):
            if self.sheet[f"B{i}"].value:
                submenu = self.get_submenu(i, max_row)
                if submenu["description"]:
                    menu["submenus"].append(submenu)
                else:
                    break
        return menu

    def parser(self) -> list[dict[str, str | list]]:
        for i in range(1, self.sheet.max_row + 1):
            if self.sheet[f"A{i}"].value:
                self.result.append(self.get_menu(i, self.sheet.max_row))
        return self.result
