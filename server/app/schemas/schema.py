from sqlmodel import (
    SQLModel,
    Field,
    Column,
    VARCHAR,
    TIMESTAMP,
    text,
    Relationship,
)
from uuid import uuid4, UUID
from pydantic import EmailStr
from datetime import datetime
from typing import List


class UserEventLink(SQLModel, table=True):
    __tablename__ = "user_event_associations"

    user_id: UUID | None = Field(foreign_key="users.id", primary_key=True)
    event_id: UUID | None = Field(foreign_key="events.id", primary_key=True)

    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        )
    )


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    firebase_uid: str = Field(unique=True)
    full_name: str
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True))
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        )
    )

    # relationship
    events: List["Event"] = Relationship(
        back_populates="users",
        link_model=UserEventLink,
    )


class Event(SQLModel, table=True):
    __tablename__ = "events"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str = Field()
    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        )
    )

    # relationship
    users: List[User] = Relationship(
        back_populates="events",
        link_model=UserEventLink,
    )


class Guest(SQLModel, table=True):
    __tablename__ = "guests"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    first_name: str = Field()
    last_name: str = Field()
    email: EmailStr | None = Field(sa_column=Column("email", VARCHAR))

    created_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
        )
    )
    updated_at: datetime = Field(
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=False,
            server_default=text("CURRENT_TIMESTAMP"),
            server_onupdate=text("CURRENT_TIMESTAMP"),
        )
    )


class Table(SQLModel, table=True):
    __tablename__ = "tables"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(default="Table 1")
    shape: str = Field(default="round")
    seats: int = Field(default=4)
    x: float = Field(default=0.0, ge=0, description="X position on canvas")
    y: float = Field(default=0.0, ge=0, description="Y position on canvas")
    width: float | None = Field(
        default=0.0, ge=0, description="Length of table on X-axis"
    )
    height: float | None = Field(
        default=0.0, ge=0, description="Length of table on Y-axis"
    )

    # relationship
    event_id: UUID | None = Field(default=None, foreign_key="events.id")


class Seat(SQLModel, table=True):
    __tablename__ = "seats"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    seat_number: int | None = Field(default=None)
    x: float = Field(default=0.0, ge=0, description="X position on canvas")
    y: float = Field(default=0.0, ge=0, description="Y position on canvas")

    # relationship
    table_id: UUID = Field(foreign_key="tables.id")
    guest_id: UUID | None = Field(default=None, foreign_key="guests.id")
