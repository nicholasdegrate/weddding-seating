from pydantic import BaseModel, EmailStr


class CreateUserRequest(BaseModel):
    full_name: str
    email: EmailStr
