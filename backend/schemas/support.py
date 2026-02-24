from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Support Case Schemas
class SupportCaseBase(BaseModel):
    user_id: int
    description: str
    status: str
    resolution_note: str

class SupportCaseCreate(BaseModel):
    description: str

class SupportCaseUpdate(BaseModel):
    status: str
    resolution_note: str

class SupportCaseResponse(SupportCaseBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Entry Log Schemas
class EntryLogBase(BaseModel):
    ticket_id: int
    status: str

class EntryLogResponse(EntryLogBase):
    id: int
    entry_time: datetime

    class Config:
        from_attributes = True

# Ticket Validation Schemas
class TicketValidateRequest(BaseModel):
    ticket_code: str

class TicketValidateResponse(BaseModel):
    is_valid: bool
    message: str
    ticket_info: Optional[dict] = None
