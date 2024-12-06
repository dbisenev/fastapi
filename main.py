import uvicorn
import httpx
from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security.utils import get_authorization_scheme_param
from api import router as router_v1
from external_api import router as external_router
from core.models import Base, db_helper
from core.config import settings, BASE_URL
from contextlib import asynccontextmanager
from auth import router as auth_router
from auth.utils import decode_access_token
from auth.dependency import get_current_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_prefix)
app.include_router(router=external_router, prefix=settings.api_prefix)
app.include_router(router=auth_router, prefix=settings.api_prefix)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):

    public_routes = ["/api/v1/auth/login", "/api/v1/auth/register", "/docs", "/openapi.json"]
    if request.url.path in public_routes:
        return await call_next(request)

    authorization: str = request.headers.get("Authorization")
    scheme, token = get_authorization_scheme_param(authorization)

    if not authorization or scheme.lower() != "bearer":
        return JSONResponse(
            status_code=401,
            content={"detail":"Not authenticated"},
            headers={"WWW-Authenticate":"Bearer"}
        )

    payload = decode_access_token(token)
    if not payload:
        return JSONResponse(
                status_code=401,
                content={"detail": "Invalid or expired token"},
                headers={"WWW-Authenticate": "Bearer"},
            )


    request.state.user = payload.get("sub")

    return await call_next(request)


@app.get("/test/")
async def get_products(current_user: str=Depends(get_current_user)):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/products")
        response.raise_for_status()
        return response.json()

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)