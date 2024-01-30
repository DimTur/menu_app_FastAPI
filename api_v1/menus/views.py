import pickle

from fastapi import (
    APIRouter,
    Depends,
    status,
    HTTPException,
    BackgroundTasks,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from . import crud
from .cache_crud import MenuService

from .dependencies import menu_by_id
from .schemas import Menu, MenuCreate, MenuUpdatePartial

from core.redis.redis_helper import cache

router = APIRouter(tags=["Menus"])


async def get_list_menus_cache(redis_client, key):
    if (cached_menus := redis_client.get(key)) is not None:
        return pickle.loads(cached_menus)
    return None


async def set_list_menus_cache(redis_client, key, data):
    await redis_client.set(key, pickle.dumps(data))


async def get_all_menus(
    redis_client,
    session,
    cache_key,
    crud_func,
):
    cached_data = await get_list_menus_cache(redis_client, cache_key)
    if cached_data is not None:
        return cached_data

    data = await crud_func(session=session)
    await set_list_menus_cache(redis_client, cache_key, data)
    return data


@router.get("/", response_model=list[Menu])
async def get_menus(
    redis_client: cache = Depends(cache),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    cache_key = "list_menus"
    menus = await get_all_menus(
        redis_client=redis_client,
        session=session,
        cache_key=cache_key,
        crud_func=crud.get_menus,
    )
    return menus


# @router.get("/", response_model=list[Menu])
# async def get_menus(
#     redis_client: cache = Depends(cache),
#     session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     if (cached_menus := redis_client.get("menus")) is not None:
#         return pickle.loads(cached_menus)
#
#     menus = await crud.get_menus(session=session)
#     redis_client.set("menus", pickle.dumps(menus))
#     return menus


# @router.get("/", response_model=list[Menu])
# async def get_menus(
#     background_tasks: BackgroundTasks,
#     repo: MenuService = Depends(),
# ):
#     return await repo.get_all_menus(background_tasks=background_tasks)


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
