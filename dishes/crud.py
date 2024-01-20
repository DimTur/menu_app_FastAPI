from dishes.schemas import CreateDish


def create_dish(dish_in: CreateDish) -> dict:
    dish = dish_in.model_dump()
    return {
        "success": True,
        "dish": dish,
    }
