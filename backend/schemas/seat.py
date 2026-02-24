from pydantic import BaseModel
from typing import Optional

class SeatBase(BaseModel):
    seat_number: str
    status: str
    event_id: int

class SeatResponse(SeatBase):
    id: int

    class Config:
        from_attributes = True

class SeatUpdate(BaseModel):
    status: str
