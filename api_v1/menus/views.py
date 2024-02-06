from fastapi import APIRouter, Depends, status

from .dependencies import menu_by_id, menu_by_id_not_from_cache
from .schemas import Menu, MenuCreate, MenuUpdatePartial
from .service_repository import MenuService

router = APIRouter(tags=["Menus"])


@router.get(
    "/",
    response_model=list[Menu],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список всех меню",
)
async def get_menus(repo: MenuService = Depends()):
    return await repo.get_all_menus()


@router.post(
    "/",
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового меню",
)
async def create_menu(
    menu_in: MenuCreate,
    repo: MenuService = Depends(),
):
    return await repo.create_menu(menu_in)


@router.get(
    "/{menu_id}",
    response_model=Menu,
    status_code=status.HTTP_200_OK,
    summary="Возвращает меню по его id",
)
async def get_menu_by_id(
    menu: Menu = Depends(menu_by_id_not_from_cache),
):
    return menu


@router.patch(
    "/{menu_id}",
    response_model=MenuUpdatePartial,
    status_code=status.HTTP_200_OK,
    summary="Обновление меню по его id",
)
async def update_menu_partial(
    menu_update: MenuUpdatePartial,
    menu: Menu = Depends(menu_by_id_not_from_cache),
    repo: MenuService = Depends(),
):
    return await repo.update_menu(menu=menu, menu_update=menu_update)


@router.delete(
    "/{menu_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаление меню по его id",
)
async def delete_menu(
    menu: Menu = Depends(menu_by_id),
    repo: MenuService = Depends(),
) -> None:
    return await repo.delete_menu(menu=menu)
