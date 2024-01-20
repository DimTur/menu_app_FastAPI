from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class CreateDish(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(32)]
    description: Annotated[str, MinLen(3), MaxLen(300)]
    price: float
