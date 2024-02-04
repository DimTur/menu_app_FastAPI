import uuid
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class SubmenuBase(BaseModel):
    """Базовая схема подменю"""

    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]


class SubmenuCreate(SubmenuBase):
    """Схема для создания подменю"""

    pass


class SubmenuUpdate(SubmenuCreate):
    """Схема для обновления подменю"""

    pass


class SubmenuUpdatePartial(SubmenuCreate):
    """Схема для частичного обновления подменю"""

    pass


class Submenu(SubmenuBase):
    """Базовая схема подменю с id"""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dishes_count: int = 0
