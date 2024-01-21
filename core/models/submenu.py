import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.models import Base


class Submenu(Base):
    __tablename__ = "submenus"

    menu_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("menus.id"),
    )
