import uuid
from decimal import Decimal
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class DishBase(BaseModel):
    """Базовая схема блюд"""

    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]
    price: Decimal | None


class DishCreate(DishBase):
    """Схема для создания блюда"""

    pass


class DishUpdate(DishBase):
    """Схема для обновления блюда"""

    pass


class DishUpdatePartial(DishCreate):
    """Схема для частичного обновления блюда"""

    pass


class Dish(DishBase):
    """Базовая схема блюд с id"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
