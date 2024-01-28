from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import pool, QueuePool, NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncConnection,
)

from core.config import settings
from core.models import Base


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False, poolclass: str = None):
        if poolclass is None:
            poolclass = QueuePool
        else:
            poolclass = getattr(pool, poolclass)

        self.engine = create_async_engine(
            url=url,
            echo=echo,
            poolclass=poolclass,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def get_scoped_session(self):
        session = async_scoped_session(
            session_factory=self.session_factory,
            scopefunc=current_task,
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session
            await session.close()

    async def scoped_session_dependency(self) -> AsyncSession:
        session = self.get_scoped_session()
        yield session
        await session.close()

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        async with self.engine.begin() as connection:
            yield connection

    # Используется для тестов
    async def create_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection):
        await connection.run_sync(Base.metadata.drop_all)


db_helper = DatabaseHelper(
    url=settings.db.url,
    echo=settings.db.echo,
    poolclass=settings.db.poolclass,
)
