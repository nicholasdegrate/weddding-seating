from fastapi import APIRouter

from .events import event_router

event_router = APIRouter()
event_router.include_router(event_router, tags=["events"])

__all__ = ["event_router"]
