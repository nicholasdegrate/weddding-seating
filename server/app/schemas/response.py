import uuid
from datetime import datetime

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str


class EventResponse(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime


class TableResponse(BaseModel):
    id: str
    x: int
    y: int
    height: int
    width: int
    shape: str
    name: str
