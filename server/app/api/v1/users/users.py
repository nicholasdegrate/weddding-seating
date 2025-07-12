from fastapi import APIRouter, Depends, status

from app.cors.dependencies.base import get_current_user
from app.schemas.response import UserResponse
from app.schemas.schema import User

user_router = APIRouter()

@user_router.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_user)):
    return current_user


@user_router.post("/", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: User,
        
):
    pass
