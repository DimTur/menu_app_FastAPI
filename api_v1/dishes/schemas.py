import uuid
from decimal import Decimal
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]
    price: Decimal | None


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class DishUpdatePartial(DishCreate):
    pass


class Dish(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
