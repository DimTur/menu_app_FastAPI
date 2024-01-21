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

router = APIRouter(tags=["Submenus"])

from . import crud
from .schemas import Submenu, SubmenuBase, SubmenuCreate


@router.get("/", response_model=list[Submenu])
async def get_submenus(
    menu_id: Annotated[uuid.UUID, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_submenus(session=session, menu_id=menu_id)


@router.post(
    "/",
    response_model=Submenu,
    status_code=status.HTTP_201_CREATED,
)
async def create_submenu(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_in: SubmenuCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_submenu(
        session=session, menu_id=menu_id, submenu_in=submenu_in
    )
