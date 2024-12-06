from fastapi import APIRouter

from .views import router as auth_router

router = APIRouter()
router.include_router(router=auth_router, prefix="/auth")