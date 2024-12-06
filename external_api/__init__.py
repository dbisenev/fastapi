from fastapi import APIRouter

from .view import router as imported_products_router

router = APIRouter()
router.include_router(router=imported_products_router, prefix="/imported_products")