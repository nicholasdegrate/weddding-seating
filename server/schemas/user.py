from pydantic import BaseModel, EmailStr, Field
from uuid import UUID


class User(BaseModel):
    id: int
    full_name: str

    email: EmailStr


class UserCreate(BaseModel):
    id: int = UUID(10)
    name: str = Field(..., min=1)
    email: EmailStr = Field()
