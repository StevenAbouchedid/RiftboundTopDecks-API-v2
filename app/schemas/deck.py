"""Deck schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID


class DeckCardBase(BaseModel):
    """Base deck card schema"""
    card_id: int
    quantity: int = Field(..., gt=0)
    section: str = Field(..., pattern="^(legend|battlefield|rune|main|side)$")


class DeckBase(BaseModel):
    """Base deck schema"""
    name: str = Field(..., max_length=255)
    format_id: Optional[int] = None
    description: Optional[str] = None
    visibility: str = Field(default="public", pattern="^(public|unlisted|private)$")


class DeckCreate(DeckBase):
    """Schema for creating a deck"""
    cards: list[DeckCardBase] = []


class DeckCardResponse(DeckCardBase):
    """Schema for deck card response"""
    id: int
    deck_id: int
    
    class Config:
        from_attributes = True


class DeckResponse(DeckBase):
    """Schema for deck response"""
    id: int
    user_id: Optional[UUID] = None
    legend: Optional[str] = None
    size: int
    is_user_deck: bool
    hidden: bool
    view_count: int
    trending_score: Optional[float] = None
    trending_updated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    cards: list[DeckCardResponse] = []
    
    class Config:
        from_attributes = True


class DeckValidationResponse(BaseModel):
    """Schema for deck validation response"""
    is_valid: bool
    errors: list[str] = []


class DeckListResponse(BaseModel):
    """Schema for paginated deck list"""
    data: list[DeckResponse]
    total: int
    page: int
    page_size: int
    
    class Config:
        from_attributes = True
