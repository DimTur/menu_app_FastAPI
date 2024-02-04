import uuid
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict


class SubmenuBase(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(0), MaxLen(300)]


class SubmenuCreate(SubmenuBase):
    pass


class SubmenuUpdate(SubmenuCreate):
    pass


class SubmenuUpdatePartial(SubmenuCreate):
    # title: Annotated[str, MinLen(3), MaxLen(32)] | None = None
    # description: Annotated[str, MinLen(0), MaxLen(300)] | None = None
    pass


class Submenu(SubmenuBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    dishes_count: int = 0
