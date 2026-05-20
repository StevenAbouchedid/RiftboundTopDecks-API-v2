"""Format API routes"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.format import Format
from app.models.card import Card
from app.schemas.format import FormatResponse

router = APIRouter()


@router.get("/formats", response_model=list[FormatResponse])
async def list_formats(db: Session = Depends(get_db)):
    """List all formats"""
    formats = db.query(Format).all()
    return formats


@router.get("/formats/{format_id}", response_model=FormatResponse)
async def get_format(format_id: int, db: Session = Depends(get_db)):
    """Get format by ID"""
    format = db.query(Format).filter(Format.id == format_id).first()
    
    if not format:
        raise HTTPException(status_code=404, detail="Format not found")
    
    return format


@router.get("/formats/{format_id}/legal-cards")
async def get_legal_cards(format_id: int, db: Session = Depends(get_db)):
    """Get all legal cards in a format"""
    format = db.query(Format).filter(Format.id == format_id).first()
    
    if not format:
        raise HTTPException(status_code=404, detail="Format not found")
    
    # Get legal sets for this format
    legal_sets = [fs.set_name for fs in format.format_sets]
    
    # Get all cards from legal sets
    cards = db.query(Card).filter(Card.set.in_(legal_sets)).all()
    
    return {
        "format": format.name,
        "legal_sets": legal_sets,
        "card_count": len(cards),
        "cards": cards
    }
