import uuid

from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession

from app.api.v1.events.models import (
    get_all_events_by_user,
    get_event_by_user,
    delete_event_by_user,
    create_event_by_user,
    update_event_by_user,
)
from app.cors.dependencies.base import (
    get_current_user,
)
from app.db import get_session
from app.schemas.request import CreateEventRequest, UpdateEventRequest
from app.schemas.response import EventResponse
from app.schemas.schema import User

event_router = APIRouter()


@event_router.get("/", response_model=EventResponse)
async def get_events(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await get_all_events_by_user(current_user.id, session)


@event_router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await get_event_by_user(current_user.id, event_id, session)


@event_router.post(
    "/", response_model=CreateEventRequest, status_code=status.HTTP_201_CREATED
)
async def create_event(
    payload: CreateEventRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await create_event_by_user(payload, current_user.id, session)


@event_router.delete("/", response_model=EventResponse)
async def delete_event(
    event_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await delete_event_by_user(event_id, current_user.id, session)


@event_router.patch(
    "/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK
)
async def update_event(
    payload: UpdateEventRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    return await update_event_by_user(payload, current_user.id, session)
