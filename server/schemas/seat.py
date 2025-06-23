from pydantic import BaseModel, Field
from typing import Optional, List, Literal
import uuid as UUID


class ChairBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., example="Table 5")
    shape: Literal["round", "rectangle", "oval"]
    seats: int = Field(..., ge=1, example=8)
    x: float = Field(..., ge=0, description="X position on canvas")
    y: float = Field(..., ge=0, description="Y position on canvas")
    width: float = Field(..., g=0, description="Length of table on X-axis")
    height: float = Field(..., g=0, description="Length of table on Y-axis")


class DefaultChair(BaseModel):
    name: str = "Unnamed Table"
    shape: "round"
    seats: 4
    x: 0
    y: 0
    width: 1
    height: 1
