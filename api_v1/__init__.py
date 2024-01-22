from fastapi import APIRouter

from .menus.views import router as menus_router
from .submenus.views import router as submenus_router
from .dishes.views import router as dishes_router

router = APIRouter()
router.include_router(router=menus_router, prefix="/menus")
router.include_router(router=submenus_router, prefix="/menus/{menu_id}/submenus")
router.include_router(
    router=dishes_router, prefix="/menus/{menu_id}/submenus/{submenu_id}"
)
