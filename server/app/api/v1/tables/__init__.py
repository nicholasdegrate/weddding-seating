from fastapi import APIRouter

from .table import table_router

table_router = APIRouter()
table_router.include_router(table_router, tags=["table"])

__all__ = ["table_router"]
