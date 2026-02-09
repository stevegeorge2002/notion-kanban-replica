"""FastAPI backend for Kanban board."""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session

from .database import get_db, init_db
from .models import BoardColumn, Card

app = FastAPI(title="Notion Kanban API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic schemas
class ColumnCreate(BaseModel):
    title: str
    color: Optional[str] = "#e9e9e7"


class ColumnResponse(BaseModel):
    id: int
    title: str
    position: int
    color: str
    
    class Config:
        from_attributes = True


class CardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: int
    color: Optional[str] = "#ffffff"


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    column_id: Optional[int] = None
    position: Optional[int] = None
    color: Optional[str] = None


class CardMove(BaseModel):
    column_id: int
    position: int


class CardResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    column_id: int
    position: int
    color: str
    
    class Config:
        from_attributes = True


# Database dependency
def get_db_session():
    with get_db() as db:
        yield db


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


# Column endpoints
@app.get("/api/columns", response_model=List[ColumnResponse])
def get_columns(db: Session = Depends(get_db_session)):
    """Get all columns."""
    columns = db.query(BoardColumn).order_by(BoardColumn.position).all()
    return columns


@app.post("/api/columns", response_model=ColumnResponse)
def create_column(column: ColumnCreate, db: Session = Depends(get_db_session)):
    """Create a new column."""
    max_position = db.query(BoardColumn).count()
    db_column = BoardColumn(
        title=column.title,
        color=column.color,
        position=max_position
    )
    db.add(db_column)
    db.commit()
    db.refresh(db_column)
    return db_column


@app.delete("/api/columns/{column_id}")
def delete_column(column_id: int, db: Session = Depends(get_db_session)):
    """Delete a column."""
    column = db.query(BoardColumn).filter(BoardColumn.id == column_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    
    db.delete(column)
    db.commit()
    return {"message": "Column deleted successfully"}


# Card endpoints
@app.get("/api/cards", response_model=List[CardResponse])
def get_cards(column_id: Optional[int] = None, db: Session = Depends(get_db_session)):
    """Get all cards, optionally filtered by column."""
    query = db.query(Card)
    if column_id:
        query = query.filter(Card.column_id == column_id)
    cards = query.order_by(Card.position).all()
    return cards


@app.post("/api/cards", response_model=CardResponse)
def create_card(card: CardCreate, db: Session = Depends(get_db_session)):
    """Create a new card."""
    # Get max position in column
    max_position = db.query(Card).filter(Card.column_id == card.column_id).count()
    
    db_card = Card(
        title=card.title,
        description=card.description,
        column_id=card.column_id,
        position=max_position,
        color=card.color
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


@app.put("/api/cards/{card_id}", response_model=CardResponse)
def update_card(card_id: int, card: CardUpdate, db: Session = Depends(get_db_session)):
    """Update a card."""
    db_card = db.query(Card).filter(Card.id == card_id).first()
    if not db_card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    if card.title is not None:
        db_card.title = card.title
    if card.description is not None:
        db_card.description = card.description
    if card.color is not None:
        db_card.color = card.color
    
    db.commit()
    db.refresh(db_card)
    return db_card


@app.delete("/api/cards/{card_id}")
def delete_card(card_id: int, db: Session = Depends(get_db_session)):
    """Delete a card."""
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    db.delete(card)
    db.commit()
    return {"message": "Card deleted successfully"}


@app.patch("/api/cards/{card_id}/move", response_model=CardResponse)
def move_card(card_id: int, move: CardMove, db: Session = Depends(get_db_session)):
    """Move a card to a different column and position."""
    card = db.query(Card).filter(Card.id == card_id).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    
    old_column_id = card.column_id
    old_position = card.position
    
    # Update card
    card.column_id = move.column_id
    card.position = move.position
    
    # Reorder cards in old column
    if old_column_id != move.column_id:
        cards_in_old_column = db.query(Card).filter(
            Card.column_id == old_column_id,
            Card.position > old_position
        ).all()
        for c in cards_in_old_column:
            c.position -= 1
    
    # Reorder cards in new column
    cards_in_new_column = db.query(Card).filter(
        Card.column_id == move.column_id,
        Card.position >= move.position,
        Card.id != card_id
    ).all()
    for c in cards_in_new_column:
        c.position += 1
    
    db.commit()
    db.refresh(card)
    return card


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Notion Kanban API", "version": "1.0.0"}
