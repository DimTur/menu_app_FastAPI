import uuid

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

# за счет этой конструкции мы избегаем циклических импортов
if TYPE_CHECKING:
    from .menu import Submenu


class Dish(Base):
    __tablename__ = "dishes"

    price: Mapped[float] = mapped_column(Float(precision=2))
    submenu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("submenus.id"),
    )
    submenu: Mapped["Submenu"] = relationship(back_populates="dishes")

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r})"

    def __repr__(self):
        return str(self)

    @property
    def formatted_price(self) -> Optional[str]:
        if self.price is not None:
            return f"{self.price:.2f}"
        return None
