import uuid
from typing import List
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.request import CreateEventRequest, UpdateEventRequest
from app.schemas.response import TableResponse
from app.schemas.schema import Event, UserEventLink, Table


async def get_all_events_by_user(user_id: UUID, session: AsyncSession):
    stmt = (
        select(Event)
        .join(UserEventLink, UserEventLink.event_id == Event.id)
        .where(UserEventLink.user_id == user_id)
    )

    result = await session.exec(stmt)
    return result.all()


async def get_event_by_user(user_id: UUID, event_id: UUID, session: AsyncSession):
    stmt = (
        select(Event)
        .join(UserEventLink, UserEventLink.event_id == Event.id)
        .where(and_(UserEventLink.user_id == user_id, Event.id == event_id))
    )

    result = await session.exec(stmt)
    event = result.first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found or access denied",
        )
    return event


async def delete_event_by_user(event_id: UUID, user_id: UUID, session: AsyncSession):
    db_event = await session.get(Event, event_id)

    if not db_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    stmt = (
        select(Event)
        .join(UserEventLink, UserEventLink.event_id == Event.id)
        .where(and_(UserEventLink.user_id == user_id, Event.id == event_id))
    )

    result = await session.exec(stmt)
    event = result.first()

    if db_event.id != event.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    await session.delete(db_event)
    await session.commit()

    return db_event


async def create_event_by_user(
    payload: CreateEventRequest, user_id: uuid.UUID, session: AsyncSession
):
    try:
        event = Event(**payload.model_dump())
        link = UserEventLink(user_id=user_id, event_id=event.id)
        session.add_all([event, link])
        await session.commit()
        return event
    except IntegrityError:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unexpected error occurred while creating event.",
        )
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating event.",
        )


async def update_event_by_user(
    payload: UpdateEventRequest, user_id: uuid.UUID, session: AsyncSession
):
    try:
        event = await session.get(Event, payload.id)
        if not event:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected error occurred while creating event.",
            )

        stmt = select(UserEventLink).where(
            UserEventLink.event_id == event.id, UserEventLink.user_id == user_id
        )

        result = await session.exec(stmt)
        link = result.first()
        if not link:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Unauthorized error",
            )

        event_to_update = payload.model_dump(exclude_unset=True)
        for key, value in event_to_update.items():
            setattr(event, key, value)

        session.add(event)
        await session.commit()
        await session.refresh(event)

        return event
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating event.",
        )


async def get_tables_by_event(
    event_id, user_id: uuid.UUID, session: AsyncSession
) -> List[TableResponse]:
    try:
        event = await session.get(Event, event_id)

        if not event:
            HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Current Event can not be found",
            )

        stmt = select(UserEventLink).where(
            UserEventLink.event_id == event_id, UserEventLink.user_id == user_id
        )

        result = await session.exec(stmt)
        is_valid_linked = result.first()
        if not is_valid_linked:
            HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized user"
            )

        stmt_table = select(Table).where(Table.event_id == event_id)
        table_result = await session.exec(stmt_table)

        return table_result.all()
    except Exception:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred while creating event.",
        )
