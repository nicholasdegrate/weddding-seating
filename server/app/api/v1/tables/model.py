import uuid

from fastapi import status, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.request import CreateTableRequest
from app.schemas.schema import Table, UserEventLink


async def create_table_by_event(
    payload: CreateTableRequest, user_id: uuid.UUID, session: AsyncSession
):
    try:
        stmt = select(UserEventLink).where(
            UserEventLink.event_id == payload.event_id,
            UserEventLink.user_id == payload.user_id,
        )

        result = await session.exec(stmt)

        if not result.first():
            raise HTTPException()
        table = Table(**payload.model_dump())
    except Exception:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="")
