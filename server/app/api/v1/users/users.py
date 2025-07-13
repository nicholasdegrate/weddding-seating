from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from app.cors.dependencies.base import (
    get_current_user,
    FirebaseClaims,
    get_firebase_claims,
)
from app.db import get_session
from app.schemas.request import CreateUserRequest
from app.schemas.response import UserResponse
from app.schemas.schema import User

user_router = APIRouter()


@user_router.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUserRequest,
    claims: FirebaseClaims = Depends(get_firebase_claims),
    session: AsyncSession = Depends(get_session),
):
    db_user = User(**payload.model_dump(), firebase_uid=claims.uid)
    session.add(db_user)
    try:
        await session.commit()
        await session.refresh(db_user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Internal System Error",
        )
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating user.",
        )
    return db_user
