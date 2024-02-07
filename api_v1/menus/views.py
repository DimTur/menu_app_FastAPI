from fastapi import APIRouter, Depends, status

from .dependencies import menu_by_id, menu_by_id_not_from_cache
from .responses import (
    delete_menu_by_id_responses,
    get_all_menus_responses,
    get_menu_by_id_responses,
    patch_menu_by_id_responses,
    post_menu_responses,
)
from .schemas import Menu, MenuCreate, MenuUpdatePartial
from .service_repository import MenuService

router = APIRouter(tags=["Menus"])


@router.get(
    "/all/",
    response_model=list[Menu],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список всех меню",
    responses=get_all_menus_responses,
)
async def get_all_base(repo: MenuService = Depends()) -> list[Menu]:
    return await repo.get_all_base()


@router.get(
    "/",
    response_model=list[Menu],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список всех меню",
    responses=get_all_menus_responses,
)
async def get_menus(repo: MenuService = Depends()) -> list[Menu]:
    return await repo.get_all_menus()


@router.post(
    "/",
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового меню",
    responses=post_menu_responses,
)
async def create_menu(
    menu_in: MenuCreate,
    repo: MenuService = Depends(),
) -> Menu:
    return await repo.create_menu(menu_in)


@router.get(
    "/{menu_id}",
    response_model=Menu,
    status_code=status.HTTP_200_OK,
    summary="Возвращает меню по его id",
    responses=get_menu_by_id_responses,
)
async def get_menu_by_id(
    menu: Menu = Depends(menu_by_id_not_from_cache),
) -> Menu:
    return menu


@router.patch(
    "/{menu_id}",
    response_model=MenuUpdatePartial,
    status_code=status.HTTP_200_OK,
    summary="Обновление меню по его id",
    responses=patch_menu_by_id_responses,
)
async def update_menu_partial(
    menu_update: MenuUpdatePartial,
    menu: Menu = Depends(menu_by_id_not_from_cache),
    repo: MenuService = Depends(),
) -> Menu:
    return await repo.update_menu(menu=menu, menu_update=menu_update)


@router.delete(
    "/{menu_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаление меню по его id",
    responses=delete_menu_by_id_responses,
)
async def delete_menu(
    menu: Menu = Depends(menu_by_id),
    repo: MenuService = Depends(),
) -> None:
    return await repo.delete_menu(menu=menu)
