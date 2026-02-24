from pydantic import BaseModel
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

class OfferBase(BaseModel):
    code: str
    discount_percent: Decimal
    max_discount_amount: Decimal
    expiry_date: date
    is_active: bool
    usage_limit: int

class OfferCreate(OfferBase):
    pass

class OfferResponse(OfferBase):
    id: int
    used_count: int
    created_at: datetime

    class Config:
        from_attributes = True
