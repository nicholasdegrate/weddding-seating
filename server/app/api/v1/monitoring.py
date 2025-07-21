from fastapi import APIRouter
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from fastapi import status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db import get_session
from app.schemas.schema import User

monitoring_router = APIRouter()


@monitoring_router.get("/ping", tags=["server-health"])
async def ping():
    """_summary_

    showcase the status of server 'on' or 'off'
    """
    return JSONResponse(content={"ping": "pong"}, status_code=status.HTTP_200_OK)


@monitoring_router.get("/healthz", tags=["health"])
async def healthz(session: AsyncSession = Depends(get_session)):
    """_summary_

    showcase the status of third party deps
    example: SQL database/redis
    """
    try:
        db_status = await session.exec(select(User))
        if db_status.first() is not None:
            return JSONResponse(
                content={"status": "healthy"}, status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "unhealthy"},
            )
    except Exception:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content={"status": "error"}
        )
