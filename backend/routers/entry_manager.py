from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database.database import get_db
from models.ticket import Ticket
from models.entry_log import EntryLog
from models.seat import Seat
from models.event import Event
from schemas.support import TicketValidateRequest, TicketValidateResponse, EntryLogResponse
from utils.auth import check_role

router = APIRouter(prefix="/entry", tags=["Entry Manager"])

@router.post("/validate-ticket", response_model=TicketValidateResponse)
def validate_ticket(req: TicketValidateRequest, db: Session = Depends(get_db), current_user=Depends(check_role(["entry_manager", "admin"]))):
    ticket = db.query(Ticket).filter(Ticket.ticket_code == req.ticket_code).first()
    
    if not ticket:
        return TicketValidateResponse(is_valid=False, message="Invalid ticket code")
    
    if ticket.status != "Confirmed":
        return TicketValidateResponse(is_valid=False, message=f"Ticket is {ticket.status}")
    
    # Check if already used
    used_log = db.query(EntryLog).filter(EntryLog.ticket_id == ticket.id, EntryLog.status == "Success").first()
    if used_log:
        return TicketValidateResponse(is_valid=False, message="Ticket already used")
    
    # Check event date
    seat = db.query(Seat).filter(Seat.id == ticket.seat_id).first()
    event = db.query(Event).filter(Event.id == seat.event_id).first()
    
    if event.event_date < datetime.now().date():
         return TicketValidateResponse(is_valid=False, message="Ticket expired (Event past)")

    # If all good, mark as used and log entry
    ticket.status = "Used"
    new_log = EntryLog(
        ticket_id=ticket.id,
        status="Success"
    )
    db.add(new_log)
    db.commit()
    
    return TicketValidateResponse(
        is_valid=True,
        message="Ticket validated successfully",
        ticket_info={
            "ticket_code": ticket.ticket_code,
            "event": event.name,
            "seat": seat.seat_number
        }
    )
