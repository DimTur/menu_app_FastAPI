
from fastapi import APIRouter

from .menus.views import router as menus_router

router = APIRouter()
router.include_router(router=menus_router, prefix="/menus")
