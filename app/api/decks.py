"""Deck API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
from app.database import get_db
from app.models.deck import Deck, DeckCard
from app.schemas.deck import DeckCreate, DeckResponse, DeckValidationResponse, DeckListResponse

router = APIRouter()


@router.get("/decks", response_model=DeckListResponse)
async def list_decks(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    legend: Optional[str] = None,
    format_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """List decks with pagination"""
    query = db.query(Deck).filter(Deck.visibility == 'public', Deck.hidden == False)
    
    if legend:
        query = query.filter(Deck.legend == legend)
    
    if format_id:
        query = query.filter(Deck.format_id == format_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    decks = query.offset(offset).limit(page_size).all()
    
    return DeckListResponse(
        data=decks,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/decks/{deck_id}", response_model=DeckResponse)
async def get_deck(deck_id: int, db: Session = Depends(get_db)):
    """Get deck by ID"""
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    # Increment view count
    deck.view_count += 1
    db.commit()
    
    return deck


@router.post("/decks", response_model=DeckResponse, status_code=201)
async def create_deck(deck: DeckCreate, db: Session = Depends(get_db)):
    """Create a new deck"""
    # Create deck
    db_deck = Deck(
        name=deck.name,
        format_id=deck.format_id,
        description=deck.description,
        visibility=deck.visibility,
        is_user_deck=True
    )
    db.add(db_deck)
    db.flush()  # Get deck ID
    
    # Add cards
    for card in deck.cards:
        db_deck_card = DeckCard(
            deck_id=db_deck.id,
            card_id=card.card_id,
            quantity=card.quantity,
            section=card.section
        )
        db.add(db_deck_card)
    
    db.commit()
    db.refresh(db_deck)
    
    return db_deck


@router.put("/decks/{deck_id}", response_model=DeckResponse)
async def update_deck(deck_id: int, deck: DeckCreate, db: Session = Depends(get_db)):
    """Update a deck"""
    db_deck = db.query(Deck).filter(Deck.id == deck_id).first()
    
    if not db_deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    # Update deck fields
    db_deck.name = deck.name
    db_deck.format_id = deck.format_id
    db_deck.description = deck.description
    db_deck.visibility = deck.visibility
    
    # Delete existing cards
    db.query(DeckCard).filter(DeckCard.deck_id == deck_id).delete()
    
    # Add new cards
    for card in deck.cards:
        db_deck_card = DeckCard(
            deck_id=deck_id,
            card_id=card.card_id,
            quantity=card.quantity,
            section=card.section
        )
        db.add(db_deck_card)
    
    db.commit()
    db.refresh(db_deck)
    
    return db_deck


@router.delete("/decks/{deck_id}", status_code=204)
async def delete_deck(deck_id: int, db: Session = Depends(get_db)):
    """Delete a deck"""
    db_deck = db.query(Deck).filter(Deck.id == deck_id).first()
    
    if not db_deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    db.delete(db_deck)
    db.commit()
    
    return None


@router.post("/decks/{deck_id}/validate", response_model=DeckValidationResponse)
async def validate_deck(deck_id: int, db: Session = Depends(get_db)):
    """Validate a deck against game rules"""
    # Check deck exists
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    
    if not deck:
        raise HTTPException(status_code=404, detail="Deck not found")
    
    # Call database validation function
    result = db.execute(
        text("SELECT * FROM validate_deck(:deck_id)"),
        {"deck_id": deck_id}
    ).fetchone()
    
    is_valid, errors = result
    
    return DeckValidationResponse(
        is_valid=is_valid,
        errors=errors if errors else []
    )
