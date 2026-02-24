from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RefundRequestBase(BaseModel):
    order_id: int
    reason: str
    status: str

class RefundRequestCreate(BaseModel):
    order_id: int
    reason: str

class RefundRequestUpdate(BaseModel):
    status: str

class RefundRequestResponse(RefundRequestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
