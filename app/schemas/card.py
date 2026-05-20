"""Card schemas"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CardBase(BaseModel):
    """Base card schema"""
    name: str = Field(..., max_length=255)
    set: str = Field(..., max_length=100)
    card_number: Optional[str] = Field(None, max_length=50)
    type: str = Field(..., max_length=100)
    domains: Optional[list[str]] = None
    runes: Optional[int] = None
    power: Optional[int] = None
    might: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    rarity: Optional[str] = Field(None, max_length=50)
    artist: Optional[str] = Field(None, max_length=255)
    image_url: Optional[str] = None


class CardCreate(CardBase):
    """Schema for creating a card"""
    base_card_id: Optional[int] = None
    is_alt_art: bool = False
    is_signature: bool = False
    tcgplayer_product_id: Optional[int] = None


class CardResponse(CardBase):
    """Schema for card response"""
    id: int
    base_card_id: Optional[int] = None
    is_alt_art: bool
    is_signature: bool
    tcgplayer_product_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CardListResponse(BaseModel):
    """Schema for paginated card list"""
    cards: list[CardResponse]
    total: int
    page: int
    page_size: int
    
    class Config:
        from_attributes = True
