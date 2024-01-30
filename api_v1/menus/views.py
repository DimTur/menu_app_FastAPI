import pickle

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud

from .dependencies import menu_by_id
from .schemas import Menu, MenuCreate, MenuUpdatePartial

from core.redis.redis_helper import cache

router = APIRouter(tags=["Menus"])


@router.get("/", response_model=list[Menu])
async def get_menus(
    redis_client: cache = Depends(cache),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    if (cached_menus := redis_client.get("menus")) is not None:
        return pickle.loads(cached_menus)

    menus = await crud.get_menus(session=session)
    redis_client.set("menus", pickle.dumps(menus))
    return menus


@router.post(
    "/",
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    menu_in: MenuCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_menu(session=session, menu_in=menu_in)


@router.get("/{menu_id}", response_model=Menu)
async def get_menu_by_id(
    menu: Menu = Depends(menu_by_id),
):
    return menu


@router.patch("/{menu_id}")
async def update_menu_partial(
    menu_update: MenuUpdatePartial,
    menu: Menu = Depends(menu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_menu(
        session=session,
        menu=menu,
        menu_update=menu_update,
        partial=True,
    )


@router.delete(
    "/{menu_id}",
    # status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_menu(
    menu: Menu = Depends(menu_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> None:
    await crud.delete_menu(
        session=session,
        menu=menu,
    )
