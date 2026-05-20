"""Deck models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, TIMESTAMP, Float, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base


class Deck(Base):
    """Deck model"""
    __tablename__ = "decks"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Ownership
    user_id = Column(UUID(as_uuid=True), index=True)
    
    # Deck identity
    name = Column(String(255), nullable=False)
    format_id = Column(Integer, ForeignKey("formats.id"), index=True)
    
    # Computed fields (maintained by triggers)
    legend = Column(String(100), index=True)
    size = Column(Integer, default=0)
    
    # Metadata
    description = Column(Text)
    
    # Visibility
    visibility = Column(String(20), default='public', index=True)
    is_user_deck = Column(Boolean, nullable=False, default=True)
    hidden = Column(Boolean, default=False)
    
    # Engagement
    view_count = Column(Integer, default=0)
    trending_score = Column(Float)
    trending_updated_at = Column(TIMESTAMP)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now(), index=True)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Constraints
    __table_args__ = (
        CheckConstraint("visibility IN ('public', 'unlisted', 'private')", name='check_visibility'),
    )
    
    # Relationships
    deck_cards = relationship("DeckCard", back_populates="deck", cascade="all, delete-orphan")
    format = relationship("Format", back_populates="decks")
    event_decks = relationship("EventDeck", back_populates="deck")


class DeckCard(Base):
    """Deck card junction model"""
    __tablename__ = "deck_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    deck_id = Column(Integer, ForeignKey("decks.id", ondelete="CASCADE"), nullable=False, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    section = Column(String(50), nullable=False, index=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("quantity > 0", name='check_quantity_positive'),
        CheckConstraint("section IN ('legend', 'battlefield', 'rune', 'main', 'side')", name='check_section'),
    )
    
    # Relationships
    deck = relationship("Deck", back_populates="deck_cards")
    card = relationship("Card", back_populates="deck_cards")
