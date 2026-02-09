"""Standalone Kanban Board - No dependencies on app folder."""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from contextlib import contextmanager

# Database setup
Base = declarative_base()
DATABASE_URL = "sqlite:///./kanban.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class BoardColumn(Base):
    __tablename__ = "columns"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    color = Column(String(7), default="#e9e9e7")
    created_at = Column(DateTime, default=datetime.utcnow)
    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    column_id = Column(Integer, ForeignKey("columns.id"), nullable=False)
    position = Column(Integer, nullable=False)
    color = Column(String(7), default="#ffffff")
    created_at = Column(DateTime, default=datetime.utcnow)
    column = relationship("BoardColumn", back_populates="cards")


# Create tables
Base.metadata.create_all(bind=engine)


@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Pydantic models
class ColumnCreate(BaseModel):
    title: str
    color: Optional[str] = "#e9e9e7"


class CardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: int


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class CardMove(BaseModel):
    column_id: int
    position: int


# FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# API Endpoints
@app.get("/api/columns")
def get_columns():
    with get_db() as db:
        columns = db.query(BoardColumn).order_by(BoardColumn.position).all()
        return [{"id": c.id, "title": c.title, "position": c.position, "color": c.color} for c in columns]


@app.post("/api/columns")
def create_column(column: ColumnCreate):
    with get_db() as db:
        max_position = db.query(BoardColumn).count()
        db_column = BoardColumn(title=column.title, color=column.color, position=max_position)
        db.add(db_column)
        db.commit()
        db.refresh(db_column)
        return {"id": db_column.id, "title": db_column.title, "position": db_column.position, "color": db_column.color}


@app.delete("/api/columns/{column_id}")
def delete_column(column_id: int):
    with get_db() as db:
        column = db.query(BoardColumn).filter(BoardColumn.id == column_id).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")
        db.delete(column)
        db.commit()
        return {"message": "Column deleted"}


@app.get("/api/cards")
def get_cards():
    with get_db() as db:
        cards = db.query(Card).order_by(Card.position).all()
        return [{"id": c.id, "title": c.title, "description": c.description, "column_id": c.column_id, "position": c.position, "color": c.color} for c in cards]


@app.post("/api/cards")
def create_card(card: CardCreate):
    with get_db() as db:
        max_position = db.query(Card).filter(Card.column_id == card.column_id).count()
        db_card = Card(title=card.title, description=card.description, column_id=card.column_id, position=max_position)
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return {"id": db_card.id, "title": db_card.title, "description": db_card.description, "column_id": db_card.column_id, "position": db_card.position, "color": db_card.color}


@app.put("/api/cards/{card_id}")
def update_card(card_id: int, card: CardUpdate):
    with get_db() as db:
        db_card = db.query(Card).filter(Card.id == card_id).first()
        if not db_card:
            raise HTTPException(status_code=404, detail="Card not found")
        if card.title:
            db_card.title = card.title
        if card.description is not None:
            db_card.description = card.description
        db.commit()
        db.refresh(db_card)
        return {"id": db_card.id, "title": db_card.title, "description": db_card.description, "column_id": db_card.column_id, "position": db_card.position, "color": db_card.color}


@app.patch("/api/cards/{card_id}/move")
def move_card(card_id: int, move: CardMove):
    with get_db() as db:
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        card.column_id = move.column_id
        card.position = move.position
        db.commit()
        db.refresh(card)
        return {"id": card.id, "title": card.title, "description": card.description, "column_id": card.column_id, "position": card.position, "color": card.color}


# Frontend HTML (same as before - the long HTML string)
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notion Kanban Board</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #ffffff; color: #37352f; }
        .header { padding: 24px 32px; border-bottom: 1px solid #e3e2e0; display: flex; justify-content: space-between; align-items: center; }
        h1 { font-size: 28px; font-weight: 700; }
        .board { padding: 24px 32px; display: flex; gap: 16px; overflow-x: auto; height: calc(100vh - 100px); }
        .column { min-width: 280px; max-width: 320px; background: #f7f6f3; border-radius: 6px; border: 1px solid #e3e2e0; }
        .column-header { padding: 12px 16px; background: #e9e9e7; border-radius: 6px 6px 0 0; display: flex; justify-content: space-between; align-items: center; }
        .column-title { font-size: 14px; font-weight: 600; }
        .column-actions { display: flex; gap: 4px; opacity: 0; transition: opacity 0.2s; }
        .column:hover .column-actions { opacity: 1; }
        .cards { padding: 16px; min-height: 200px; }
        .card { background: #ffffff; border-radius: 3px; padding: 12px; margin-bottom: 8px; border: 1px solid #e3e2e0; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12); cursor: grab; transition: all 0.2s; }
        .card:hover { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15); border-color: #d3d2d0; }
        .card.dragging { opacity: 0.5; cursor: grabbing; }
        .card-title { font-size: 14px; font-weight: 500; line-height: 1.5; margin-bottom: 4px; }
        .card-description { font-size: 12px; color: #787774; line-height: 1.4; }
        button { background: transparent; border: none; cursor: pointer; padding: 4px 8px; border-radius: 4px; font-size: 13px; transition: all 0.2s; }
        button:hover { background: rgba(0, 0, 0, 0.05); }
        .btn-primary { background: #2383e2; color: white; padding: 8px 16px; }
        .btn-primary:hover { background: #1a6bc4; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); justify-content: center; align-items: center; z-index: 1000; }
        .modal.active { display: flex; }
        .modal-content { background: white; padding: 24px; border-radius: 8px; max-width: 500px; width: 90%; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.24); }
        .modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; }
        .modal-title { font-size: 18px; font-weight: 600; }
        .form-group { margin-bottom: 16px; }
        label { display: block; font-size: 13px; font-weight: 500; margin-bottom: 4px; }
        input, textarea { width: 100%; padding: 8px 12px; border: 1px solid #e3e2e0; border-radius: 4px; font-family: inherit; font-size: 14px; }
        input:focus, textarea:focus { outline: none; border-color: #2383e2; box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.1); }
        textarea { resize: vertical; min-height: 100px; }
        .modal-actions { display: flex; gap: 8px; justify-content: flex-end; }
        .empty-state { text-align: center; color: #9b9a97; padding: 24px; font-size: 12px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Kanban Board</h1>
        <button class="btn-primary" onclick="openColumnModal()">+ Add Column</button>
    </div>
    <div class="board" id="board"></div>
    <div class="modal" id="cardModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title" id="cardModalTitle">Create Card</h2>
                <button onclick="closeCardModal()">✕</button>
            </div>
            <form id="cardForm" onsubmit="saveCard(event)">
                <div class="form-group"><label>Title</label><input type="text" id="cardTitle" required></div>
                <div class="form-group"><label>Description</label><textarea id="cardDescription"></textarea></div>
                <input type="hidden" id="cardId"><input type="hidden" id="cardColumnId">
                <div class="modal-actions">
                    <button type="button" onclick="closeCardModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Save</button>
                </div>
            </form>
        </div>
    </div>
    <div class="modal" id="columnModal">
        <div class="modal-content">
            <div class="modal-header"><h2 class="modal-title">Create Column</h2><button onclick="closeColumnModal()">✕</button></div>
            <form id="columnForm" onsubmit="saveColumn(event)">
                <div class="form-group"><label>Column Name</label><input type="text" id="columnTitle" required></div>
                <div class="modal-actions">
                    <button type="button" onclick="closeColumnModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Create</button>
                </div>
            </form>
        </div>
    </div>
    <script>
        let columns = []; let cards = []; let draggedCard = null;
        async function loadData() { const [colsRes, cardsRes] = await Promise.all([fetch('/api/columns'), fetch('/api/cards')]); columns = await colsRes.json(); cards = await cardsRes.json(); renderBoard(); }
        function renderBoard() { const board = document.getElementById('board'); board.innerHTML = ''; columns.forEach(col => { const columnEl = document.createElement('div'); columnEl.className = 'column'; columnEl.innerHTML = `<div class="column-header"><span class="column-title">${col.title}</span><div class="column-actions"><button onclick="openCardModal(${col.id})">+</button><button onclick="deleteColumn(${col.id})">🗑️</button></div></div><div class="cards" data-column-id="${col.id}" ondragover="allowDrop(event)" ondrop="drop(event, ${col.id})">${getCardsForColumn(col.id)}</div>`; board.appendChild(columnEl); }); }
        function getCardsForColumn(columnId) { const columnCards = cards.filter(c => c.column_id === columnId); if (columnCards.length === 0) return '<p class="empty-state">Drop cards here</p>'; return columnCards.map(card => `<div class="card" draggable="true" ondragstart="drag(event, ${card.id})" ondragend="dragEnd(event)"><div class="card-title">${card.title}</div>${card.description ? `<div class="card-description">${card.description}</div>` : ''}</div>`).join(''); }
        function drag(event, cardId) { draggedCard = cardId; event.target.classList.add('dragging'); }
        function dragEnd(event) { event.target.classList.remove('dragging'); }
        function allowDrop(event) { event.preventDefault(); }
        async function drop(event, columnId) { event.preventDefault(); if (!draggedCard) return; await fetch(`/api/cards/${draggedCard}/move`, { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ column_id: columnId, position: 0 }) }); draggedCard = null; await loadData(); }
        function openCardModal(columnId, cardId = null) { document.getElementById('cardModal').classList.add('active'); document.getElementById('cardColumnId').value = columnId; if (cardId) { const card = cards.find(c => c.id === cardId); document.getElementById('cardModalTitle').textContent = 'Edit Card'; document.getElementById('cardId').value = cardId; document.getElementById('cardTitle').value = card.title; document.getElementById('cardDescription').value = card.description || ''; } else { document.getElementById('cardModalTitle').textContent = 'Create Card'; document.getElementById('cardId').value = ''; document.getElementById('cardTitle').value = ''; document.getElementById('cardDescription').value = ''; } }
        function closeCardModal() { document.getElementById('cardModal').classList.remove('active'); }
        async function saveCard(event) { event.preventDefault(); const cardId = document.getElementById('cardId').value; const data = { title: document.getElementById('cardTitle').value, description: document.getElementById('cardDescription').value, column_id: parseInt(document.getElementById('cardColumnId').value) }; if (cardId) { await fetch(`/api/cards/${cardId}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }); } else { await fetch('/api/cards', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }); } closeCardModal(); await loadData(); }
        function openColumnModal() { document.getElementById('columnModal').classList.add('active'); document.getElementById('columnTitle').value = ''; }
        function closeColumnModal() { document.getElementById('columnModal').classList.remove('active'); }
        async function saveColumn(event) { event.preventDefault(); const title = document.getElementById('columnTitle').value; await fetch('/api/columns', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ title }) }); closeColumnModal(); await loadData(); }
        async function deleteColumn(columnId) { if (!confirm('Delete this column and all its cards?')) return; await fetch(`/api/columns/${columnId}`, { method: 'DELETE' }); await loadData(); }
        loadData();
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)