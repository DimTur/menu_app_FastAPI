import uuid
from decimal import Decimal
from typing import Annotated, Union, Optional
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]
    price: Optional[Decimal]


class DishCreate(DishBase):
    pass


class DishUpdate(DishBase):
    pass


class DishUpdatePartial(DishCreate):
    title: Annotated[str, MinLen(3), MaxLen(32)] | None = None
    description: Annotated[str, MinLen(0), MaxLen(300)] | None = None
    price: Optional[Decimal] | None = None


class Dish(DishBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
