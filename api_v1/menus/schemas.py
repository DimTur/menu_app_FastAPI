import uuid
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class MenuBase(BaseModel):
    """Базовая схема меню"""

    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]


class MenuCreate(MenuBase):
    """Схема для создания меню"""

    pass


class MenuUpdate(MenuCreate):
    """Схема для обновления меню"""

    pass


class MenuUpdatePartial(MenuCreate):
    """Схема для частичного обновления меню"""

    pass


class Menu(MenuBase):
    """Базовая схема меню с id"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    submenus_count: int = 0
    dishes_count: int = 0
