import uuid
import pickle
from typing import Annotated

from fastapi import (
    Path,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, Menu
from core.redis import cache

from . import crud


class EntityDoesNotExist(Exception):
    """Raised when entity was not found in database."""


async def menu_by_id(
    menu_id: Annotated[uuid.UUID, Path],
    redis_client: cache = Depends(cache),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Menu:
    if (cached_menu := redis_client.get(f"menu_{menu_id}")) is not None:
        return pickle.loads(cached_menu)
    try:
        menu = await crud.get_menu_by_id(session=session, menu_id=menu_id)
        redis_client.set(f"menu_{menu_id}", pickle.dumps(menu))

        return menu

    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"menu not found",
        )
