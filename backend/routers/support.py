from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.support_case import SupportCase
from models.refund_request import RefundRequest
from models.order import Order
from models.ticket import Ticket
from models.seat import Seat
from schemas.support import SupportCaseResponse, SupportCaseUpdate
from schemas.refund import RefundRequestResponse, RefundRequestUpdate
from utils.auth import check_role

router = APIRouter(prefix="/support", tags=["Support Executive"])

@router.get("/cases", response_model=List[SupportCaseResponse])
def list_cases(db: Session = Depends(get_db), current_user=Depends(check_role(["support", "admin"]))):
    return db.query(SupportCase).all()

@router.patch("/cases/{case_id}", response_model=SupportCaseResponse)
def update_case(case_id: int, case_update: SupportCaseUpdate, db: Session = Depends(get_db), current_user=Depends(check_role(["support", "admin"]))):
    case = db.query(SupportCase).filter(SupportCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    case.status = case_update.status
    case.resolution_note = case_update.resolution_note
    db.commit()
    db.refresh(case)
    return case

@router.get("/refunds", response_model=List[RefundRequestResponse])
def list_refunds(db: Session = Depends(get_db), current_user=Depends(check_role(["support", "admin"]))):
    return db.query(RefundRequest).all()

@router.patch("/refunds/{refund_id}", response_model=RefundRequestResponse)
def handle_refund(refund_id: int, refund_update: RefundRequestUpdate, db: Session = Depends(get_db), current_user=Depends(check_role(["support", "admin"]))):
    refund = db.query(RefundRequest).filter(RefundRequest.id == refund_id).first()
    if not refund:
        raise HTTPException(status_code=404, detail="Refund request not found")
    
    refund.status = refund_update.status
    
    if refund_update.status == "Approved":
        # Business rules: update order, seat, and ticket
        order = db.query(Order).filter(Order.id == refund.order_id).first()
        order.order_status = "Refunded"
        
        tickets = db.query(Ticket).filter(Ticket.order_id == order.id).all()
        for ticket in tickets:
            ticket.status = "Cancelled"
            seat = db.query(Seat).filter(Seat.id == ticket.seat_id).first()
            seat.status = "Available"
            
    db.commit()
    db.refresh(refund)
    return refund
