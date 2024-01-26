import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.db_helper import db_helper

from main import app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with db_helper.connect() as conn:
        await db_helper.drop_all(conn)
        await db_helper.create_all(conn)


async def override_scoped_session_dependency() -> AsyncSession:
    session = db_helper.get_scoped_session()
    yield session
    await session.close()


app.dependency_overrides[
    db_helper.scoped_session_dependency
] = override_scoped_session_dependency


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
