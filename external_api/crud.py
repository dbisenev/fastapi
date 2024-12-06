import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.models import Product
from api.products.schemas import ProductCreate

async def import_products_from_api(
    session: AsyncSession,
    api_url: str
) -> list[Product]:
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        response.raise_for_status()
        products_data = response.json()

    imported_products = []

    for product_data in products_data:
        query = select(Product).where(
            Product.name == product_data["title"],
            Product.price == int(product_data["price"])
        )
        result = await session.execute(query)
        existing_product = result.scalar_one_or_none()

        if existing_product:
            imported_products.append(existing_product)
        else:
            product_in = ProductCreate(
                name=product_data["title"],
                description=product_data["description"],
                price=int(product_data["price"])
            )
            product = Product(**product_in.model_dump())
            session.add(product)
            imported_products.append(product)

    await session.commit()
    return imported_products
