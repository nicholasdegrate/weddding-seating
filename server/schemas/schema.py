from sqlmodel import SQLModel, Field, Column, VARCHAR
from typing import Literal
from uuid import uuid4
from pydantic import EmailStr


class User(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    full_name: str
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True))


class Table(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    name: str = Field(default="Table 1")
    shape: Literal["round", "rectangle", "oval"] = Field(default="round")
    seats: int = Field(default=4)
    x: float = Field(default=0.0, ge=0, description="X position on canvas")
    y: float = Field(default=0.0, ge=0, description="Y position on canvas")
    width: float | None = Field(
        default=0.0, ge=0, description="Length of table on X-axis"
    )
    height: float | None = Field(
        default=0.0, ge=0, description="Length of table on Y-axis"
    )


class Chair(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    name: str
    shape: Literal["single", "bench"] | None = Field(default="round")
    seats: int | None = Field(default=1)
    x: float = Field(default=0.0, ge=0, description="X position on canvas")
    y: float = Field(default=0.0, ge=0, description="Y position on canvas")
    width: float | None = Field(
        default=0.0, ge=0, description="Length of table on X-axis"
    )
    height: float | None = Field(
        default=0.0, ge=0, description="Length of table on Y-axis"
    )


class Venue(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    name: str
    width: float | None = Field(
        default=0.0, ge=0, description="Length of table on X-axis"
    )
    height: float | None = Field(
        default=0.0, ge=0, description="Length of table on Y-axis"
    )
