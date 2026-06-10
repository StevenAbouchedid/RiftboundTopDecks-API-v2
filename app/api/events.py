"""Event API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from app.database import get_db
from app.models.event import Event
from app.schemas.event import EventResponse, EventListResponse

router = APIRouter()


@router.get("/events", response_model=EventListResponse)
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    format_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """List events with pagination"""
    query = db.query(Event)
    
    if format_id:
        query = query.filter(Event.format_id == format_id)
    
    if start_date:
        query = query.filter(Event.event_date >= start_date)
    
    if end_date:
        query = query.filter(Event.event_date <= end_date)
    
    # Order by date descending
    query = query.order_by(Event.event_date.desc())
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    events = query.offset(offset).limit(page_size).all()
    
    return EventListResponse(
        data=events,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, db: Session = Depends(get_db)):
    """Get event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    return event


@router.get("/events/{event_id}/decks")
async def get_event_decks(
    event_id: int,
    top_n: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get event results (decks with placements)"""
    event = db.query(Event).filter(Event.id == event_id).first()
    
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Get event decks ordered by placement
    event_decks = event.event_decks
    event_decks.sort(key=lambda x: x.placement)
    
    # Limit to top N if specified
    if top_n:
        event_decks = event_decks[:top_n]
    
    return event_decks
