import uuid

from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr


class CreateEventRequest(BaseModel):
    title: str


class UpdateEventRequest(BaseModel):
    id: uuid.UUID
    title: str


class CreateTableRequest(BaseModel):
    x: int
    y: int
    height: int
    width: int
    title: str
    shape: str
    seats: int
    event_id: uuid.UUID
