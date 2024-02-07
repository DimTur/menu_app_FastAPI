import uuid
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict

from api_v1.dishes.schemas import Dish


class SubmenuBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuCreate):
    pass


class SubmenuUpdatePartial(SubmenuCreate):
    pass


class Submenu(SubmenuBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dishes_count: int = 0


class FullBaseSubmenu(Submenu):
    dishes: list[Dish]
