from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .utils import create_access_token, verify_password, hash_password
from core.models.users import User
from core.models import db_helper
from .schemes import UserCreate, UserLogin, Token

router = APIRouter(tags=['Auth'])

@router.post("/register", status_code=201)
async def register(user: UserCreate, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    query = select(User).where(User.username == user.username)
    result = await session.execute(query)
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    session.add(new_user)
    await session.commit()
    return {"message": "User registered successfully"}


@router.post("/login", response_model=Token)
async def login(user: UserLogin, session: AsyncSession = Depends(db_helper.get_scoped_session)):
    query = select(User).where(User.username == user.username)
    result = await session.execute(query)
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid username or password"
        )

    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}