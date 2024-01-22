import uuid
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Path,
    status,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper

# from .dependencies import submenu_by_id

router = APIRouter(tags=["Dishes"])

from . import crud
from .schemas import Dish


@router.get("/", response_model=list[Dish])
async def get_dishes(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_dishes(
        session=session,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
