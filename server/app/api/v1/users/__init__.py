from fastapi import APIRouter

from .users import user_router

users_router = APIRouter()
users_router.include_router(user_router, tags=["users"])

__all__ = ["users_router"]