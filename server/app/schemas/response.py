from pydantic import BaseModel, Field
import uuid


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: str
