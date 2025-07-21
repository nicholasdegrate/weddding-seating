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
