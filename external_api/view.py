from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession



from . import crud
from core.models import db_helper

router = APIRouter(tags=["External"])

@router.post("/import/", status_code= status.HTTP_201_CREATED)
async def import_products(
    api_url: str = "https://fakestoreapi.com/products",
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    imported_products = await crud.import_products_from_api(
        session=session,
        api_url=api_url
    )
    return {"message": f"Imported {len(imported_products)} products", "products": imported_products}