from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Dish(Base):
    __tablename__ = "dishes"

    price: Mapped[float] = mapped_column(Float(precision=2))
