# from pydantic import BaseModel, Field
# from typing import Optional, List, Literal
from sqlmodel import SQLModel
from pydantic import Field
from typing import Literal
from uuid import uuid4


class User(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    full_name: str | None = Field(default="John Doe")
    email: str | None


class Table(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    name: str | None = Field(default="Table 1")
    shape: Literal["round", "rectangle", "oval"] | None = Field(default="round")
    seats: int | None = Field(default=4)
    x: float | None = Field(default=0.0, g=0,description="X position on canvas")
    y: float | None = Field(default=0.0, g=0,description="Y position on canvas")
    width: float | None = Field(default=0.0, g=0, description="Length of table on X-axis")
    height: float | None = Field(default=0.0, g=0, description="Length of table on Y-axis")

class Chair(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    name: str
    shape: Literal["single", "bench"] | None = Field(default="round")
    seats: int | None = Field(default=1)
    x: float | None = Field(default=0.0, g=0,description="X position on canvas")
    y: float | None = Field(default=0.0, g=0,description="Y position on canvas")
    width: float | None = Field(default=0.0, g=0, description="Length of Chair on X-axis")
    height: float | None = Field(default=0.0, g=0, description="Length of Chair on Y-axis")

class Venue(SQLModel, table=True):
    id: int | None = Field(default=uuid4, primary_key=True)
    name: str
    width: float | None = Field(default=0.0, g=0, description="Length of Chair on X-axis")
    height: float | None = Field(default=0.0, g=0, description="Length of Chair on Y-axis")