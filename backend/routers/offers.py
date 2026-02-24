from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.offer import Offer
from schemas.offer import OfferCreate, OfferResponse
from utils.auth import check_role

router = APIRouter(prefix="/offers", tags=["Offers"])

@router.post("/", response_model=OfferResponse)
def create_offer(offer_in: OfferCreate, db: Session = Depends(get_db), current_user=Depends(check_role(["admin"]))):
    new_offer = Offer(**offer_in.model_dump())
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer

@router.get("/", response_model=List[OfferResponse])
def list_offers(db: Session = Depends(get_db)):
    return db.query(Offer).all()
