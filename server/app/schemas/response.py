from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    id: str
    email: str = Field(..., example="john.doe@example.com")
    full_name: str = Field(..., example="john doe")

    class Config:
        orm_mode = True