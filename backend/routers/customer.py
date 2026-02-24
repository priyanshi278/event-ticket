from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from database.database import get_db
from models.user import User
from models.event import Event
from models.seat import Seat
from models.order import Order
from models.ticket import Ticket
from models.offer import Offer
from models.refund_request import RefundRequest
from models.support_case import SupportCase
from schemas.event import EventResponse
from schemas.seat import SeatResponse
from schemas.order import OrderCreate, OrderResponse
from schemas.refund import RefundRequestCreate, RefundRequestResponse
from schemas.support import SupportCaseCreate, SupportCaseResponse
from utils.auth import get_current_user, check_role

router = APIRouter(prefix="/customer", tags=["Customer"])

@router.get("/events", response_model=List[EventResponse])
def list_upcoming_events(db: Session = Depends(get_db)):
    return db.query(Event).filter(Event.status == "Open", Event.event_date >= date.today()).all()

@router.get("/events/{event_id}/seats", response_model=List[SeatResponse])
def list_available_seats(event_id: int, db: Session = Depends(get_db)):
    return db.query(Seat).filter(Seat.event_id == event_id, Seat.status == "Available").all()

@router.post("/orders", response_model=OrderResponse)
def place_order(order_in: OrderCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Basic validation
    event = db.query(Event).filter(Event.id == order_in.event_id).first()
    if not event or event.status != "Open":
        raise HTTPException(status_code=400, detail="Event not available for booking")
    
    if len(order_in.seat_ids) > event.max_tickets_per_user:
        raise HTTPException(status_code=400, detail=f"Maximum {event.max_tickets_per_user} tickets per user allowed")
    
    # Check seats
    seats = db.query(Seat).filter(Seat.id.in_(order_in.seat_ids), Seat.status == "Available").all()
    if len(seats) != len(order_in.seat_ids):
        raise HTTPException(status_code=400, detail="One or more seats are no longer available")
    
    # Calculate amounts
    total_amount = event.ticket_price * len(order_in.seat_ids)
    discount = 0
    if order_in.offer_id:
        offer = db.query(Offer).filter(Offer.id == order_in.offer_id, Offer.is_active == True, Offer.expiry_date >= date.today()).first()
        if offer:
            discount = (total_amount * offer.discount_percent) / 100
            if discount > offer.max_discount_amount:
                discount = offer.max_discount_amount
            offer.used_count += 1
    
    final_amount = total_amount - discount
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        offer_id=order_in.offer_id,
        total_amount=total_amount,
        discount_amount=discount,
        final_amount=final_amount,
        payment_mode=order_in.payment_mode,
        order_status="Completed" # Simulated checkout
    )
    db.add(new_order)
    db.flush()
    
    # Create tickets and update seats
    for seat in seats:
        seat.status = "Booked"
        ticket = Ticket(
            order_id=new_order.id,
            seat_id=seat.id,
            ticket_code=f"TC-{new_order.id}-{seat.id}",
            status="Confirmed"
        )
        db.add(ticket)
    
    db.commit()
    db.refresh(new_order)
    return new_order

@router.post("/refund-request", response_model=RefundRequestResponse)
def request_refund(refund_in: RefundRequestCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == refund_in.order_id, Order.user_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    # Check event date (rule: allowed only before event date)
    ticket = db.query(Ticket).filter(Ticket.order_id == order.id).first()
    seat = db.query(Seat).filter(Seat.id == ticket.seat_id).first()
    event = db.query(Event).filter(Event.id == seat.event_id).first()
    
    if event.event_date <= date.today():
        raise HTTPException(status_code=400, detail="Refunds are only allowed before the event date")
    
    new_request = RefundRequest(
        order_id=order.id,
        reason=refund_in.reason,
        status="Pending"
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

@router.post("/support-cases", response_model=SupportCaseResponse)
def raise_support_case(case_in: SupportCaseCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_case = SupportCase(
        user_id=current_user.id,
        description=case_in.description,
        status="Open",
        resolution_note=""
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case
