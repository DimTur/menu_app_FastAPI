from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

from .base import Base

# за счет этой конструкции мы избегаем циклических импортов
if TYPE_CHECKING:
    from .submenu import Submenu


class Menu(Base):
    __tablename__ = "menus"

    submenus: Mapped[list["Submenu"]] = relationship(
        back_populates="menu",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, title={self.title!r})"

    def __repr__(self):
        return str(self)
