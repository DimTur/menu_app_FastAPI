import uuid
from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]
    formatted_price: str


class DishCreate(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]
    price: float


class DishUpdate(DishCreate):
    pass


class DishUpdatePartial(DishCreate):
    title: Annotated[str, MinLen(3), MaxLen(32)] | None = None
    description: Annotated[str, MinLen(0), MaxLen(300)] | None = None
    price: float | None


class Dish(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
