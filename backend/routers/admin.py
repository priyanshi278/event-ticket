from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database.database import get_db
from models.venue import Venue
from models.event import Event
from schemas.event import VenueCreate, VenueResponse, EventCreate, EventUpdate, EventResponse
from utils.auth import check_role

router = APIRouter(prefix="/admin", tags=["Platform Admin"])

# Venue Management
@router.post("/venues", response_model=VenueResponse)
def create_venue(venue_in: VenueCreate, db: Session = Depends(get_db), current_user=Depends(check_role(["admin"]))):
    new_venue = Venue(**venue_in.model_dump())
    db.add(new_venue)
    db.commit()
    db.refresh(new_venue)
    return new_venue

@router.get("/venues", response_model=List[VenueResponse])
def get_venues(db: Session = Depends(get_db), current_user=Depends(check_role(["admin"]))):
    return db.query(Venue).all()

# Event Management
@router.post("/events", response_model=EventResponse)
def create_event(event_in: EventCreate, db: Session = Depends(get_db), current_user=Depends(check_role(["admin", "organizer"]))):
    new_event = Event(**event_in.model_dump())
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

@router.patch("/events/{event_id}", response_model=EventResponse)
def update_event_status(event_id: int, event_update: EventUpdate, db: Session = Depends(get_db), current_user=Depends(check_role(["admin", "organizer"]))):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    update_data = event_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event
