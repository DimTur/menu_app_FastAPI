from fastapi import (
    APIRouter,
    Depends,
    status,
)

from .service_repository import MenuService
from .dependencies import menu_by_id
from .schemas import Menu, MenuCreate, MenuUpdatePartial

router = APIRouter(tags=["Menus"])


@router.get("/", response_model=list[Menu])
async def get_menus(repo: MenuService = Depends()):
    return await repo.get_all_menus()


@router.post(
    "/",
    response_model=Menu,
    status_code=status.HTTP_201_CREATED,
)
async def create_menu(
    menu_in: MenuCreate,
    repo: MenuService = Depends(),
):
    return await repo.create_menu(menu_in)


@router.get("/{menu_id}", response_model=Menu)
async def get_menu_by_id(
    menu: Menu = Depends(menu_by_id),
):
    return menu


@router.patch("/{menu_id}")
async def update_menu_partial(
    menu_update: MenuUpdatePartial,
    menu: Menu = Depends(menu_by_id),
    repo: MenuService = Depends(),
):
    return await repo.update_menu(menu=menu, menu_update=menu_update)


@router.delete("/{menu_id}")
async def delete_menu(
    menu: Menu = Depends(menu_by_id),
    repo: MenuService = Depends(),
) -> None:
    return await repo.delete_menu(menu=menu)
