"""Card API routes"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional
from app.database import get_db
from app.models.card import Card
from app.schemas.card import CardResponse, CardListResponse

router = APIRouter()


@router.get("/cards", response_model=CardListResponse)
async def list_cards(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    card_type: Optional[str] = None,
    set_name: Optional[str] = None,
    domain: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List and search cards with pagination"""
    query = db.query(Card)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Card.name.ilike(f"%{search}%"),
                Card.description.ilike(f"%{search}%")
            )
        )
    
    if card_type:
        query = query.filter(Card.type == card_type)
    
    if set_name:
        query = query.filter(Card.set == set_name)
    
    if domain:
        # Use ANY to check if domain is in the array
        query = query.filter(Card.domains.any(domain))
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    cards = query.offset(offset).limit(page_size).all()
    
    return CardListResponse(
        data=cards,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/cards/{card_id}", response_model=CardResponse)
async def get_card(card_id: int, db: Session = Depends(get_db)):
    """Get card by ID"""
    card = db.query(Card).filter(Card.id == card_id).first()
    
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    return card


@router.get("/sets")
async def list_sets(db: Session = Depends(get_db)):
    """List all card sets"""
    sets = db.query(Card.set, func.count(Card.id)).group_by(Card.set).all()
    
    return [
        {"name": set_name, "card_count": count}
        for set_name, count in sets
    ]


@router.get("/sets/{set_name}/cards", response_model=CardListResponse)
async def list_cards_in_set(
    set_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """List all cards in a set"""
    query = db.query(Card).filter(Card.set == set_name)
    
    total = query.count()
    offset = (page - 1) * page_size
    cards = query.offset(offset).limit(page_size).all()
    
    return CardListResponse(
        cards=cards,
        total=total,
        page=page,
        page_size=page_size
    )
