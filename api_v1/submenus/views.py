import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from .dependencies import submenu_by_id, submenu_by_id_not_from_cache
from .responses import (
    delete_submenu_by_id_responses,
    get_all_submenus_responses,
    get_submenu_by_id_responses,
    patch_submenu_by_id_responses,
    post_submenu_responses,
)
from .schemas import Submenu, SubmenuCreate, SubmenuUpdatePartial
from .service_repository import SubmenuService

router = APIRouter(tags=["Submenus"])


@router.get(
    "/",
    response_model=list[Submenu],
    status_code=status.HTTP_200_OK,
    summary="Возвращает список всех подменю моню",
    responses=get_all_submenus_responses,
)
async def get_submenus(
    menu_id: Annotated[uuid.UUID, Path],
    repo: SubmenuService = Depends(),
):
    return await repo.get_all_submenus(menu_id=menu_id)


@router.post(
    "/",
    response_model=Submenu,
    status_code=status.HTTP_201_CREATED,
    summary="Создает нове подменю",
    responses=post_submenu_responses,
)
async def create_submenu(
    menu_id: Annotated[uuid.UUID, Path],
    submenu_in: SubmenuCreate,
    repo: SubmenuService = Depends(),
):
    return await repo.create_submenu(menu_id=menu_id, submenu_in=submenu_in)


@router.get(
    "/{submenu_id}",
    response_model=Submenu,
    status_code=status.HTTP_200_OK,
    summary="Возвращает подменю по его id",
    responses=get_submenu_by_id_responses,
)
async def get_submenu_bu_id(
    submenu: Submenu = Depends(submenu_by_id),
):
    return submenu


@router.patch(
    "/{submenu_id}",
    response_model=SubmenuUpdatePartial,
    status_code=status.HTTP_200_OK,
    summary="Обновляет подменю по его id",
    responses=patch_submenu_by_id_responses,
)
async def update_submenu_partial(
    submenu_update: SubmenuUpdatePartial,
    submenu: Submenu = Depends(submenu_by_id_not_from_cache),
    repo: SubmenuService = Depends(),
):
    return await repo.update_submenu(submenu=submenu, submenu_update=submenu_update)


@router.delete(
    "/{submenu_id}",
    status_code=status.HTTP_200_OK,
    summary="Удаляет подменю по его id",
    responses=delete_submenu_by_id_responses,
)
async def delete_submenu(
    submenu: Submenu = Depends(submenu_by_id_not_from_cache),
    repo: SubmenuService = Depends(),
) -> None:
    return await repo.delete_submenu(submenu=submenu)
