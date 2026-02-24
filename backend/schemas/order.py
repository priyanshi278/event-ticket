from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional, List

class OrderBase(BaseModel):
    user_id: int
    offer_id: Optional[int] = None
    total_amount: Decimal
    discount_amount: Decimal
    final_amount: Decimal
    payment_mode: str
    order_status: str

class OrderCreate(BaseModel):
    offer_id: Optional[int] = None
    event_id: int
    seat_ids: List[int]
    payment_mode: str

class OrderResponse(OrderBase):
    id: int
    booking_time: datetime

    class Config:
        from_attributes = True
