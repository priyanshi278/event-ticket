from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.event import Event
from models.seat import Seat
from models.order import Order
from schemas.seat import SeatBase, SeatResponse
from utils.auth import check_role

router = APIRouter(prefix="/organizer", tags=["Event Organizer"])

@router.post("/events/{event_id}/seats", response_model=List[SeatResponse])
def create_seats(event_id: int, seat_count: int, db: Session = Depends(get_db), current_user=Depends(check_role(["organizer", "admin"]))):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    seats = []
    for i in range(1, seat_count + 1):
        seat = Seat(seat_number=f"S-{i}", status="Available", event_id=event_id)
        seats.append(seat)
    
    db.add_all(seats)
    db.commit()
    return seats

@router.get("/events/{event_id}/booking-summary")
def get_booking_summary(event_id: int, db: Session = Depends(get_db), current_user=Depends(check_role(["organizer", "admin"]))):
    total_seats = db.query(Seat).filter(Seat.event_id == event_id).count()
    booked_seats = db.query(Seat).filter(Seat.event_id == event_id, Seat.status == "Booked").count()
    
    return {
        "event_id": event_id,
        "total_seats": total_seats,
        "booked_seats": booked_seats,
        "available_seats": total_seats - booked_seats
    }
