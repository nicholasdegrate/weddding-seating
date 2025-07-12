from fastapi import APIRouter

from .v1 import v1_router
from ..config.settings import settings

router = APIRouter()
router.include_router(v1_router, prefix=settings.api_versions.get("v1"))


__all__ = ["router"]