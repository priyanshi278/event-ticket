from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

# Venue Schemas
class VenueBase(BaseModel):
    name: str
    city: str
    address: str
    total_capacity: int

class VenueCreate(VenueBase):
    pass

class VenueResponse(VenueBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Event Schemas
class EventBase(BaseModel):
    name: str
    category: str
    event_date: date
    ticket_price: Decimal
    max_tickets_per_user: int
    status: str
    venue_id: int

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    event_date: Optional[date] = None
    ticket_price: Optional[Decimal] = None
    max_tickets_per_user: Optional[int] = None
    status: Optional[str] = None

class EventResponse(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
