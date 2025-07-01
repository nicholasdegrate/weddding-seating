from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status

monitoring_router = APIRouter()


@monitoring_router.get("/ping", tags=["server-health"])
async def ping():
    """_summary_

    showcase the status of server 'on' or 'off'

    """
    return JSONResponse(content={"ping": "pong"}, status_code=status.HTTP_200_OK)


@monitoring_router.get("/healthz", tags=["health"])
async def healthz():
    """_summary_

    showcase the status of third party deps
    example: SQL database/redis
    """
    try:
        db_status = True
        if db_status:
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
