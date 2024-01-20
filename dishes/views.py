from fastapi import APIRouter

from dishes import crud
from dishes.schemas import CreateDish

router = APIRouter(prefix="/dishes", tags=["Dishes"])


@router.post("/")
def create_dish(dish: CreateDish):
    return crud.create_dish(dish_in=dish)
