"""Event models"""
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Player(Base):
    """Player model"""
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Relationships
    event_decks = relationship("EventDeck", back_populates="player")


class Event(Base):
    """Event model"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Event identity
    name = Column(String(255), nullable=False)
    format_id = Column(Integer, ForeignKey("formats.id"), nullable=False, index=True)
    
    # Event details
    event_date = Column(Date, nullable=False, index=True)
    location = Column(String(255))
    participant_count = Column(Integer)
    status = Column(String(50))
    description = Column(Text)
    event_type = Column(String(50))
    match_format = Column(String(10), nullable=False)
    default_top_n = Column(Integer)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    format = relationship("Format", back_populates="events")
    event_decks = relationship("EventDeck", back_populates="event", cascade="all, delete-orphan")


class EventDeck(Base):
    """Event deck junction model"""
    __tablename__ = "event_decks"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    deck_id = Column(Integer, ForeignKey("decks.id", ondelete="CASCADE"), nullable=False, index=True)
    placement = Column(Integer, nullable=False, index=True)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)
    player_id = Column(Integer, ForeignKey("players.id"), index=True)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("placement > 0", name='check_placement_positive'),
    )
    
    # Relationships
    event = relationship("Event", back_populates="event_decks")
    deck = relationship("Deck", back_populates="event_decks")
    player = relationship("Player", back_populates="event_decks")
