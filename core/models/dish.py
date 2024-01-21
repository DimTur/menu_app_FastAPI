import uuid

from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Dish(Base):
    __tablename__ = "dishes"

    price: Mapped[float] = mapped_column(Float(precision=2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("submenus.id"),
    )
