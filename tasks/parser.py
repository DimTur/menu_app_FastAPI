import openpyxl


class MenuParser:
    def __init__(self, file_path):
        self.file_path = file_path

    def parse(self):
        menu_data = []
        workbook = openpyxl.load_workbook(self.file_path)
        try:
            sheet = workbook.active
            current_menu = None
            current_submenu = None

            for row in sheet.iter_rows(values_only=True):
                if row[0] and row[1] and row[2]:
                    menu_id = row[0]
                    menu_title = row[1]
                    menu_description = row[2]
                    current_menu = {
                        "title": menu_title,
                        "description": menu_description,
                        "id": menu_id,
                        "submenus": [],
                    }
                    menu_data.append(current_menu)

                elif row[1] and row[2] and row[3]:
                    submenu_id = row[1]
                    submenu_title = row[2]
                    submenu_description = row[3]
                    current_submenu = {
                        "title": submenu_title,
                        "description": submenu_description,
                        "id": submenu_id,
                        "dishes": [],
                    }
                    current_menu["submenus"].append(current_submenu)

                elif row[2] and row[3] and row[4] and row[5] and row[6]:
                    dish_id = row[2]
                    dish_title = row[3]
                    dish_description = row[4]
                    dish_price = row[5]
                    dish_discount = row[6]
                    dish = {
                        "title": dish_title,
                        "description": dish_description,
                        "price": dish_price,
                        "id": dish_id,
                        "dish_discount": dish_discount,
                    }
                    current_submenu["dishes"].append(dish)
        finally:
            workbook.close()

        return menu_data
