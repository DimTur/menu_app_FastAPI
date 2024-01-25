import uuid

from sqlalchemy import String, Text
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    declared_attr,
)


class Base(DeclarativeBase):
    __abstract__ = True

    # создает имя таблицы на основе имени текущего класса
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4, unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(32),
        unique=True,
    )
    description: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )
