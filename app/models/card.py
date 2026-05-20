"""Card models"""
from sqlalchemy import Column, Integer, String, Text, Boolean, ARRAY, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Card(Base):
    """Card model"""
    __tablename__ = "cards"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Card Identity
    name = Column(String(255), nullable=False, index=True)
    set = Column(String(100), nullable=False, index=True)
    card_number = Column(String(50))
    
    # Alt Art Support
    base_card_id = Column(Integer, ForeignKey("cards.id"), index=True)
    
    # Card Type and Domain
    type = Column(String(100), nullable=False, index=True)
    domains = Column(ARRAY(Text), index=True)
    
    # Costs and Stats
    runes = Column(Integer)
    power = Column(Integer)
    might = Column(Integer)
    
    # Card Flags
    is_alt_art = Column(Boolean, default=False, index=True)
    is_signature = Column(Boolean, default=False, index=True)
    
    # Card Text
    description = Column(Text)
    
    # Tags
    tags = Column(ARRAY(Text), index=True)
    
    # Visual Properties
    rarity = Column(String(50))
    artist = Column(String(255))
    image_url = Column(Text)
    
    # TCGPlayer Integration
    tcgplayer_product_id = Column(Integer)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    translations = relationship("CardTranslation", back_populates="card", cascade="all, delete-orphan")
    deck_cards = relationship("DeckCard", back_populates="card")
    base_card = relationship("Card", remote_side=[id], backref="alt_arts")


class CardTranslation(Base):
    """Card translation model"""
    __tablename__ = "card_translations"
    
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True)
    language = Column(String(10), nullable=False, index=True)
    
    # Translated fields
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    
    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    card = relationship("Card", back_populates="translations")
