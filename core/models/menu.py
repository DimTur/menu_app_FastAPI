from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from .base import Base

# за счет этой конструкции мы избегаем циклических импортов
if TYPE_CHECKING:
    from .submenu import Submenu


class Menu(Base):
    __tablename__ = "menus"

    submenus: Mapped[list["Submenu"]] = relationship(back_populates="menu")
