"""Format and banlist models"""
from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey, TIMESTAMP, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Format(Base):
    """Format model"""
    __tablename__ = "formats"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text)
    
    # Time period
    start_date = Column(Date)
    end_date = Column(Date, index=True)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    format_sets = relationship("FormatSet", back_populates="format", cascade="all, delete-orphan")
    format_banlists = relationship("FormatBanlist", back_populates="format", cascade="all, delete-orphan")
    decks = relationship("Deck", back_populates="format")
    events = relationship("Event", back_populates="format")


class FormatSet(Base):
    """Format set junction model"""
    __tablename__ = "format_sets"
    
    id = Column(Integer, primary_key=True, index=True)
    format_id = Column(Integer, ForeignKey("formats.id", ondelete="CASCADE"), nullable=False, index=True)
    set_name = Column(String(100), nullable=False)
    
    # Relationships
    format = relationship("Format", back_populates="format_sets")


class Banlist(Base):
    """Banlist model"""
    __tablename__ = "banlists"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    banlist_cards = relationship("BanlistCard", back_populates="banlist", cascade="all, delete-orphan")
    format_banlists = relationship("FormatBanlist", back_populates="banlist", cascade="all, delete-orphan")


class BanlistCard(Base):
    """Banlist card junction model"""
    __tablename__ = "banlist_cards"
    
    id = Column(Integer, primary_key=True, index=True)
    banlist_id = Column(Integer, ForeignKey("banlists.id", ondelete="CASCADE"), nullable=False, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    max_copies = Column(Integer, nullable=False, default=0)
    
    # Constraints
    __table_args__ = (
        CheckConstraint("max_copies >= 0", name='check_max_copies_non_negative'),
    )
    
    # Relationships
    banlist = relationship("Banlist", back_populates="banlist_cards")


class FormatBanlist(Base):
    """Format banlist junction model"""
    __tablename__ = "format_banlists"
    
    id = Column(Integer, primary_key=True, index=True)
    format_id = Column(Integer, ForeignKey("formats.id", ondelete="CASCADE"), nullable=False, index=True)
    banlist_id = Column(Integer, ForeignKey("banlists.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Relationships
    format = relationship("Format", back_populates="format_banlists")
    banlist = relationship("Banlist", back_populates="format_banlists")
