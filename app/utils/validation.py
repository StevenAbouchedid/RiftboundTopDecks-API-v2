"""
Deck validation utilities

Note: The primary validation is done by the database function validate_deck().
This Python implementation is for client-side validation or when database access is not available.
"""
from typing import Tuple
from sqlalchemy.orm import Session
from app.models.deck import Deck, DeckCard
from app.models.card import Card


def validate_deck_python(deck_id: int, db: Session) -> Tuple[bool, list[str]]:
    """
    Validate a deck against Riftbound game rules (Python implementation)
    
    This is a backup validation. The database function validate_deck() is preferred.
    
    Args:
        deck_id: ID of the deck to validate
        db: Database session
    
    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []
    
    # Get deck and cards
    deck = db.query(Deck).filter(Deck.id == deck_id).first()
    if not deck:
        return False, ["Deck not found"]
    
    deck_cards = db.query(DeckCard).filter(DeckCard.deck_id == deck_id).all()
    
    # Get card details
    card_ids = [dc.card_id for dc in deck_cards]
    cards = {c.id: c for c in db.query(Card).filter(Card.id.in_(card_ids)).all()}
    
    # 1. Check exactly 1 legend
    legend_cards = [dc for dc in deck_cards if dc.section == 'legend']
    if len(legend_cards) != 1:
        errors.append(f"Deck must have exactly 1 legend, found {len(legend_cards)}")
        return False, errors  # Can't continue without legend
    
    legend_card = cards[legend_cards[0].card_id]
    legend_domains = legend_card.domains or []
    
    # 2. Check exactly 3 unique battlefields
    battlefield_cards = [dc for dc in deck_cards if dc.section == 'battlefield']
    unique_battlefields = set()
    for dc in battlefield_cards:
        card = cards[dc.card_id]
        # Use base_card_id if available (for alt arts)
        base_id = card.base_card_id if card.base_card_id else card.id
        unique_battlefields.add(base_id)
    
    if len(unique_battlefields) != 3:
        errors.append(f"Deck must have exactly 3 unique battlefields, found {len(unique_battlefields)}")
    
    # 3. Check exactly 12 runes
    rune_cards = [dc for dc in deck_cards if dc.section == 'rune']
    rune_count = sum(dc.quantity for dc in rune_cards)
    if rune_count != 12:
        errors.append(f"Rune deck must have exactly 12 runes, found {rune_count}")
    
    # 4. Check exactly 40 main deck cards
    main_cards = [dc for dc in deck_cards if dc.section == 'main']
    main_count = sum(dc.quantity for dc in main_cards)
    if main_count != 40:
        errors.append(f"Main deck must have exactly 40 cards, found {main_count}")
    
    # 5. Check 0-8 side deck cards
    side_cards = [dc for dc in deck_cards if dc.section == 'side']
    side_count = sum(dc.quantity for dc in side_cards)
    if side_count > 8:
        errors.append(f"Side deck can have max 8 cards, found {side_count}")
    
    # 6. Check max 3 copies per card (main + side combined)
    card_counts = {}
    for dc in main_cards + side_cards:
        card = cards[dc.card_id]
        # Use base_card_id if available (for alt arts)
        base_id = card.base_card_id if card.base_card_id else card.id
        card_counts[base_id] = card_counts.get(base_id, 0) + dc.quantity
    
    for card_id, count in card_counts.items():
        if count > 3:
            card = cards.get(card_id) or cards.get(
                next(cid for cid, c in cards.items() if c.base_card_id == card_id)
            )
            errors.append(f'Card "{card.name}" has {count} copies (max 3 in main+side combined)')
    
    # 7. Check domain restrictions
    for dc in main_cards + side_cards + rune_cards:
        card = cards[dc.card_id]
        if card.domains and 'Colorless' not in card.domains:
            # Check if card domains overlap with legend domains
            if not any(d in legend_domains for d in card.domains):
                errors.append(
                    f'Card "{card.name}" (domains: {", ".join(card.domains)}) '
                    f'does not match legend domains: {", ".join(legend_domains)}'
                )
    
    # 8. Check at least 1 champion unit matching legend's first tag
    if legend_card.tags and len(legend_card.tags) > 0:
        legend_tag = legend_card.tags[0]
        champion_units = [
            dc for dc in main_cards + side_cards
            if cards[dc.card_id].type == 'Champion Unit'
            and cards[dc.card_id].tags
            and len(cards[dc.card_id].tags) > 0
            and cards[dc.card_id].tags[0] == legend_tag
        ]
        
        if not champion_units:
            errors.append(f'Deck must have at least 1 champion unit matching legend "{legend_tag}"')
    
    return len(errors) == 0, errors
