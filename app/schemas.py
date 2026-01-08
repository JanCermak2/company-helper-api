from datetime import datetime
from pydantic import BaseModel, Field
from typing import Literal

TicketStatus = Literal["open", "in_progress", "done", "canceled"]

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None


class TicketUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    status: TicketStatus | None = None


class TicketRead(BaseModel):
    id: int
    title: str
    description: str | None
    status: TicketStatus
    created_at: datetime
    updated_at: datetime

