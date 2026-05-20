"""Event schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime


class EventBase(BaseModel):
    """Base event schema"""
    name: str = Field(..., max_length=255)
    format_id: int
    event_date: date
    location: Optional[str] = Field(None, max_length=255)
    participant_count: Optional[int] = None
    status: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    event_type: Optional[str] = Field(None, max_length=50)
    match_format: str = Field(..., max_length=10)
    default_top_n: Optional[int] = None


class EventCreate(EventBase):
    """Schema for creating an event"""
    pass


class EventDeckResponse(BaseModel):
    """Schema for event deck response"""
    id: int
    event_id: int
    deck_id: int
    placement: int
    wins: Optional[int] = None
    losses: Optional[int] = None
    draws: Optional[int] = None
    player_id: Optional[int] = None
    
    class Config:
        from_attributes = True


class EventResponse(EventBase):
    """Schema for event response"""
    id: int
    created_at: datetime
    updated_at: datetime
    event_decks: list[EventDeckResponse] = []
    
    class Config:
        from_attributes = True
