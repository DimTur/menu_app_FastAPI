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
    dishes: Mapped[list["Dish"]] = relationship(back_populates="submenu")
