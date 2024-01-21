import uuid

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

# за счет этой конструкции мы избегаем циклических импортов
if TYPE_CHECKING:
    from .menu import Menu
    from .dish import Dish


class Submenu(Base):
    __tablename__ = "submenus"

    menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("menus.id"),
    )
    menu: Mapped["Menu"] = relationship(back_populates="submenus")
    dishes: Mapped[list["Dish"]] = relationship(
        back_populates="submenu",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r}, menu_id={self.menu_id})"

    def __repr__(self):
        return str(self)
