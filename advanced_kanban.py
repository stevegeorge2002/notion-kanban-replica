"""Advanced Notion Kanban Board - Production Quality."""
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
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cards = relationship("Card", back_populates="column", cascade="all, delete-orphan", order_by="Card.position")


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    column_id = Column(Integer, ForeignKey("columns.id"), nullable=False)
    position = Column(Integer, nullable=False)
    color = Column(String(7), default="#ffffff")
    tags = Column(String(500), nullable=True)  # Comma-separated tags
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    column = relationship("BoardColumn", back_populates="cards")


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


class ColumnUpdate(BaseModel):
    title: Optional[str] = None
    color: Optional[str] = None


class CardCreate(BaseModel):
    title: str
    description: Optional[str] = None
    column_id: int
    tags: Optional[str] = None


class CardUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[str] = None


class CardMove(BaseModel):
    column_id: int
    position: int


# FastAPI app
app = FastAPI(title="Notion Kanban Board API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Column Endpoints
@app.get("/api/columns")
def get_columns():
    with get_db() as db:
        columns = db.query(BoardColumn).order_by(BoardColumn.position).all()
        return [{
            "id": c.id,
            "title": c.title,
            "position": c.position,
            "color": c.color,
            "card_count": len(c.cards),
            "updated_at": c.updated_at.isoformat() if c.updated_at else None
        } for c in columns]


@app.post("/api/columns")
def create_column(column: ColumnCreate):
    with get_db() as db:
        max_position = db.query(BoardColumn).count()
        db_column = BoardColumn(title=column.title, color=column.color, position=max_position)
        db.add(db_column)
        db.commit()
        db.refresh(db_column)
        return {
            "id": db_column.id,
            "title": db_column.title,
            "position": db_column.position,
            "color": db_column.color,
            "card_count": 0
        }


@app.put("/api/columns/{column_id}")
def update_column(column_id: int, column: ColumnUpdate):
    with get_db() as db:
        db_column = db.query(BoardColumn).filter(BoardColumn.id == column_id).first()
        if not db_column:
            raise HTTPException(status_code=404, detail="Column not found")
        if column.title:
            db_column.title = column.title
        if column.color:
            db_column.color = column.color
        db.commit()
        db.refresh(db_column)
        return {"id": db_column.id, "title": db_column.title, "color": db_column.color}


@app.delete("/api/columns/{column_id}")
def delete_column(column_id: int):
    with get_db() as db:
        column = db.query(BoardColumn).filter(BoardColumn.id == column_id).first()
        if not column:
            raise HTTPException(status_code=404, detail="Column not found")
        db.delete(column)
        db.commit()
        return {"message": "Column deleted successfully"}


# Card Endpoints
@app.get("/api/cards")
def get_cards():
    with get_db() as db:
        cards = db.query(Card).order_by(Card.column_id, Card.position).all()
        return [{
            "id": c.id,
            "title": c.title,
            "description": c.description,
            "column_id": c.column_id,
            "position": c.position,
            "color": c.color,
            "tags": c.tags.split(",") if c.tags else [],
            "created_at": c.created_at.isoformat() if c.created_at else None,
            "updated_at": c.updated_at.isoformat() if c.updated_at else None
        } for c in cards]


@app.post("/api/cards")
def create_card(card: CardCreate):
    with get_db() as db:
        max_position = db.query(Card).filter(Card.column_id == card.column_id).count()
        db_card = Card(
            title=card.title,
            description=card.description,
            column_id=card.column_id,
            position=max_position,
            tags=card.tags
        )
        db.add(db_card)
        db.commit()
        db.refresh(db_card)
        return {
            "id": db_card.id,
            "title": db_card.title,
            "description": db_card.description,
            "column_id": db_card.column_id,
            "position": db_card.position,
            "tags": db_card.tags.split(",") if db_card.tags else []
        }


@app.put("/api/cards/{card_id}")
def update_card(card_id: int, card: CardUpdate):
    with get_db() as db:
        db_card = db.query(Card).filter(Card.id == card_id).first()
        if not db_card:
            raise HTTPException(status_code=404, detail="Card not found")
        if card.title is not None:
            db_card.title = card.title
        if card.description is not None:
            db_card.description = card.description
        if card.tags is not None:
            db_card.tags = card.tags
        db.commit()
        db.refresh(db_card)
        return {
            "id": db_card.id,
            "title": db_card.title,
            "description": db_card.description,
            "tags": db_card.tags.split(",") if db_card.tags else []
        }


@app.delete("/api/cards/{card_id}")
def delete_card(card_id: int):
    with get_db() as db:
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        db.delete(card)
        db.commit()
        return {"message": "Card deleted successfully"}


@app.patch("/api/cards/{card_id}/move")
def move_card(card_id: int, move: CardMove):
    with get_db() as db:
        card = db.query(Card).filter(Card.id == card_id).first()
        if not card:
            raise HTTPException(status_code=404, detail="Card not found")
        
        old_column_id = card.column_id
        old_position = card.position
        
        # Update card position
        card.column_id = move.column_id
        card.position = move.position
        
        # Reorder cards in old column
        if old_column_id != move.column_id:
            cards_in_old = db.query(Card).filter(
                Card.column_id == old_column_id,
                Card.position > old_position
            ).all()
            for c in cards_in_old:
                c.position -= 1
        
        # Reorder cards in new column
        cards_in_new = db.query(Card).filter(
            Card.column_id == move.column_id,
            Card.position >= move.position,
            Card.id != card_id
        ).all()
        for c in cards_in_new:
            c.position += 1
        
        db.commit()
        db.refresh(card)
        return {"id": card.id, "column_id": card.column_id, "position": card.position}


@app.get("/api/stats")
def get_stats():
    """Get board statistics."""
    with get_db() as db:
        total_columns = db.query(BoardColumn).count()
        total_cards = db.query(Card).count()
        return {
            "total_columns": total_columns,
            "total_cards": total_cards,
            "cards_per_column": total_cards / total_columns if total_columns > 0 else 0
        }


# Advanced Frontend HTML
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Notion Kanban Board - Advanced</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: #ffffff;
            color: #37352f;
            -webkit-font-smoothing: antialiased;
        }
        
        .header {
            padding: 20px 32px;
            border-bottom: 1px solid #e3e2e0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #ffffff;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        h1 {
            font-size: 28px;
            font-weight: 700;
            color: #37352f;
        }
        
        .header-actions {
            display: flex;
            gap: 12px;
            align-items: center;
        }
        
        .stats {
            font-size: 13px;
            color: #787774;
            padding: 6px 12px;
            background: #f7f6f3;
            border-radius: 4px;
        }
        
        .board {
            padding: 24px 32px;
            display: flex;
            gap: 16px;
            overflow-x: auto;
            height: calc(100vh - 100px);
            align-items: flex-start;
        }
        
        .column {
            min-width: 300px;
            max-width: 320px;
            background: #f7f6f3;
            border-radius: 6px;
            border: 1px solid #e3e2e0;
            flex-shrink: 0;
            transition: box-shadow 0.2s;
        }
        
        .column.drag-over {
            box-shadow: 0 0 0 2px #2383e2;
            background: #f0f7ff;
        }
        
        .column-header {
            padding: 12px 16px;
            border-radius: 6px 6px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #e3e2e0;
        }
        
        .column-title-wrapper {
            display: flex;
            align-items: center;
            gap: 8px;
            flex: 1;
        }
        
        .column-title {
            font-size: 14px;
            font-weight: 600;
            color: #37352f;
        }
        
        .card-count {
            font-size: 12px;
            color: #787774;
            background: #ffffff;
            padding: 2px 8px;
            border-radius: 12px;
        }
        
        .column-actions {
            display: flex;
            gap: 4px;
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .column:hover .column-actions {
            opacity: 1;
        }
        
        .cards {
            padding: 12px;
            min-height: 150px;
            max-height: calc(100vh - 250px);
            overflow-y: auto;
        }
        
        .card {
            background: #ffffff;
            border-radius: 3px;
            padding: 12px;
            margin-bottom: 8px;
            border: 1px solid #e3e2e0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
            cursor: grab;
            transition: all 0.2s;
            position: relative;
        }
        
        .card:hover {
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
            border-color: #d3d2d0;
            transform: translateY(-1px);
        }
        
        .card.dragging {
            opacity: 0.5;
            cursor: grabbing;
            transform: rotate(2deg);
        }
        
        .card-title {
            font-size: 14px;
            font-weight: 500;
            line-height: 1.5;
            margin-bottom: 6px;
            color: #37352f;
        }
        
        .card-description {
            font-size: 12px;
            color: #787774;
            line-height: 1.4;
            margin-bottom: 8px;
        }
        
        .card-tags {
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            margin-top: 8px;
        }
        
        .tag {
            font-size: 11px;
            padding: 2px 8px;
            background: #e3e2e0;
            border-radius: 12px;
            color: #37352f;
        }
        
        .card-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #f7f6f3;
        }
        
        .card-date {
            font-size: 11px;
            color: #9b9a97;
        }
        
        .card-actions {
            display: flex;
            gap: 4px;
            opacity: 0;
            transition: opacity 0.2s;
        }
        
        .card:hover .card-actions {
            opacity: 1;
        }
        
        button {
            background: transparent;
            border: none;
            cursor: pointer;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 13px;
            transition: all 0.2s;
            font-family: inherit;
            color: #37352f;
        }
        
        button:hover {
            background: rgba(0, 0, 0, 0.05);
        }
        
        button:active {
            transform: scale(0.98);
        }
        
        .btn-primary {
            background: #2383e2;
            color: white;
            padding: 8px 16px;
            font-weight: 500;
        }
        
        .btn-primary:hover {
            background: #1a6bc4;
        }
        
        .btn-small {
            padding: 4px 8px;
            font-size: 12px;
        }
        
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
            animation: fadeIn 0.2s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .modal.active {
            display: flex;
        }
        
        .modal-content {
            background: white;
            padding: 24px;
            border-radius: 8px;
            max-width: 540px;
            width: 90%;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.24);
            animation: slideUp 0.2s;
        }
        
        @keyframes slideUp {
            from { transform: translateY(20px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .modal-title {
            font-size: 18px;
            font-weight: 600;
            color: #37352f;
        }
        
        .close-btn {
            font-size: 20px;
            padding: 4px 8px;
        }
        
        .form-group {
            margin-bottom: 16px;
        }
        
        label {
            display: block;
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 6px;
            color: #37352f;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 10px 12px;
            border: 1px solid #e3e2e0;
            border-radius: 4px;
            font-family: inherit;
            font-size: 14px;
            transition: all 0.2s;
            color: #37352f;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #2383e2;
            box-shadow: 0 0 0 3px rgba(35, 131, 226, 0.1);
        }
        
        textarea {
            resize: vertical;
            min-height: 100px;
            line-height: 1.5;
        }
        
        .modal-actions {
            display: flex;
            gap: 8px;
            justify-content: flex-end;
            margin-top: 20px;
        }
        
        .empty-state {
            text-align: center;
            color: #9b9a97;
            padding: 32px 16px;
            font-size: 13px;
        }
        
        .color-picker {
            display: flex;
            gap: 8px;
            margin-top: 8px;
        }
        
        .color-option {
            width: 32px;
            height: 32px;
            border-radius: 4px;
            border: 2px solid transparent;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .color-option:hover {
            transform: scale(1.1);
        }
        
        .color-option.selected {
            border-color: #2383e2;
            box-shadow: 0 0 0 2px rgba(35, 131, 226, 0.2);
        }
        
        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f7f6f3;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #d3d2d0;
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #b4b3b0;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Kanban Board</h1>
        <div class="header-actions">
            <div class="stats" id="stats">Loading...</div>
            <button class="btn-primary" onclick="openColumnModal()">+ Add Column</button>
        </div>
    </div>
    
    <div class="board" id="board"></div>
    
    <!-- Card Modal -->
    <div class="modal" id="cardModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title" id="cardModalTitle">Create Card</h2>
                <button class="close-btn" onclick="closeCardModal()">×</button>
            </div>
            <form id="cardForm" onsubmit="saveCard(event)">
                <div class="form-group">
                    <label>Title *</label>
                    <input type="text" id="cardTitle" required placeholder="Enter card title...">
                </div>
                <div class="form-group">
                    <label>Description</label>
                    <textarea id="cardDescription" placeholder="Add a description (optional)..."></textarea>
                </div>
                <div class="form-group">
                    <label>Tags (comma-separated)</label>
                    <input type="text" id="cardTags" placeholder="urgent, backend, feature...">
                </div>
                <input type="hidden" id="cardId">
                <input type="hidden" id="cardColumnId">
                <div class="modal-actions">
                    <button type="button" onclick="closeCardModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Save Card</button>
                </div>
            </form>
        </div>
    </div>
    
    <!-- Column Modal -->
    <div class="modal" id="columnModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">Create Column</h2>
                <button class="close-btn" onclick="closeColumnModal()">×</button>
            </div>
            <form id="columnForm" onsubmit="saveColumn(event)">
                <div class="form-group">
                    <label>Column Name *</label>
                    <input type="text" id="columnTitle" required placeholder="Enter column name...">
                </div>
                <div class="form-group">
                    <label>Color</label>
                    <div class="color-picker">
                        <div class="color-option selected" style="background: #e9e9e7;" onclick="selectColor('#e9e9e7')"></div>
                        <div class="color-option" style="background: #ffeaa7;" onclick="selectColor('#ffeaa7')"></div>
                        <div class="color-option" style="background: #81ecec;" onclick="selectColor('#81ecec')"></div>
                        <div class="color-option" style="background: #ffb3ba;" onclick="selectColor('#ffb3ba')"></div>
                        <div class="color-option" style="background: #e0b3ff;" onclick="selectColor('#e0b3ff')"></div>
                    </div>
                    <input type="hidden" id="columnColor" value="#e9e9e7">
                </div>
                <div class="modal-actions">
                    <button type="button" onclick="closeColumnModal()">Cancel</button>
                    <button type="submit" class="btn-primary">Create Column</button>
                </div>
            </form>
        </div>
    </div>
    
    <script>
        let columns = [];
        let cards = [];
        let draggedCard = null;
        
        // Load data and stats
        async function loadData() {
            try {
                const [colsRes, cardsRes, statsRes] = await Promise.all([
                    fetch('/api/columns'),
                    fetch('/api/cards'),
                    fetch('/api/stats')
                ]);
                columns = await colsRes.json();
                cards = await cardsRes.json();
                const stats = await statsRes.json();
                
                document.getElementById('stats').textContent = 
                    `${stats.total_columns} columns · ${stats.total_cards} cards`;
                
                renderBoard();
            } catch (error) {
                console.error('Error loading data:', error);
            }
        }
        
        // Render board
        function renderBoard() {
            const board = document.getElementById('board');
            board.innerHTML = '';
            
            columns.forEach(col => {
                const columnEl = document.createElement('div');
                columnEl.className = 'column';
                columnEl.setAttribute('data-column-id', col.id);
                columnEl.innerHTML = `
                    <div class="column-header" style="background: ${col.color};">
                        <div class="column-title-wrapper">
                            <span class="column-title">${col.title}</span>
                            <span class="card-count">${col.card_count}</span>
                        </div>
                        <div class="column-actions">
                            <button class="btn-small" onclick="openCardModal(${col.id})" title="Add card">+</button>
                            <button class="btn-small" onclick="deleteColumn(${col.id})" title="Delete column">🗑</button>
                        </div>
                    </div>
                    <div class="cards" data-column-id="${col.id}" 
                         ondragover="allowDrop(event)" 
                         ondrop="drop(event, ${col.id})"
                         ondragenter="dragEnter(event)"
                         ondragleave="dragLeave(event)">
                        ${getCardsForColumn(col.id)}
                    </div>
                `;
                board.appendChild(columnEl);
            });
        }
        
        function getCardsForColumn(columnId) {
            const columnCards = cards.filter(c => c.column_id === columnId);
            if (columnCards.length === 0) {
                return '<div class="empty-state">Drop cards here or click + to add</div>';
            }
            return columnCards.map(card => {
                const tags = card.tags && card.tags.length > 0 
                    ? `<div class="card-tags">${card.tags.map(tag => `<span class="tag">${tag.trim()}</span>`).join('')}</div>`
                    : '';
                const date = card.created_at ? new Date(card.created_at).toLocaleDateString() : '';
                
                return `
                    <div class="card" draggable="true" 
                         ondragstart="drag(event, ${card.id})"
                         ondragend="dragEnd(event)">
                        <div class="card-title">${card.title}</div>
                        ${card.description ? `<div class="card-description">${card.description}</div>` : ''}
                        ${tags}
                        <div class="card-footer">
                            <span class="card-date">${date}</span>
                            <div class="card-actions">
                                <button class="btn-small" onclick="openCardModal(${card.column_id}, ${card.id})">✏️</button>
                                <button class="btn-small" onclick="deleteCard(${card.id})">🗑</button>
                            </div>
                        </div>
                    </div>
                `;
            }).join('');
        }
        
        // Drag and drop
        function drag(event, cardId) {
            draggedCard = cardId;
            event.target.classList.add('dragging');
        }
        
        function dragEnd(event) {
            event.target.classList.remove('dragging');
        }
        
        function allowDrop(event) {
            event.preventDefault();
        }
        
        function dragEnter(event) {
            const column = event.target.closest('.column');
            if (column) column.classList.add('drag-over');
        }
        
        function dragLeave(event) {
            const column = event.target.closest('.column');
            if (column && !column.contains(event.relatedTarget)) {
                column.classList.remove('drag-over');
            }
        }
        
        async function drop(event, columnId) {
            event.preventDefault();
            const column = event.target.closest('.column');
            if (column) column.classList.remove('drag-over');
            
            if (!draggedCard) return;
            
            await fetch(`/api/cards/${draggedCard}/move`, {
                method: 'PATCH',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ column_id: columnId, position: 0 })
            });
            
            draggedCard = null;
            await loadData();
        }
        
        // Card modal
        function openCardModal(columnId, cardId = null) {
            document.getElementById('cardModal').classList.add('active');
            document.getElementById('cardColumnId').value = columnId;
            
            if (cardId) {
                const card = cards.find(c => c.id === cardId);
                document.getElementById('cardModalTitle').textContent = 'Edit Card';
                document.getElementById('cardId').value = cardId;
                document.getElementById('cardTitle').value = card.title;
                document.getElementById('cardDescription').value = card.description || '';
                document.getElementById('cardTags').value = card.tags ? card.tags.join(', ') : '';
            } else {
                document.getElementById('cardModalTitle').textContent = 'Create Card';
                document.getElementById('cardId').value = '';
                document.getElementById('cardTitle').value = '';
                document.getElementById('cardDescription').value = '';
                document.getElementById('cardTags').value = '';
            }
            
            // Focus title input
            setTimeout(() => document.getElementById('cardTitle').focus(), 100);
        }
        
        function closeCardModal() {
            document.getElementById('cardModal').classList.remove('active');
        }
        
        async function saveCard(event) {
            event.preventDefault();
            const cardId = document.getElementById('cardId').value;
            const data = {
                title: document.getElementById('cardTitle').value,
                description: document.getElementById('cardDescription').value,
                column_id: parseInt(document.getElementById('cardColumnId').value),
                tags: document.getElementById('cardTags').value
            };
            
            try {
                if (cardId) {
                    await fetch(`/api/cards/${cardId}`, {
                        method: 'PUT',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                } else {
                    await fetch('/api/cards', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(data)
                    });
                }
                
                closeCardModal();
                await loadData();
            } catch (error) {
                console.error('Error saving card:', error);
                alert('Error saving card. Please try again.');
            }
        }
        
        async function deleteCard(cardId) {
            if (!confirm('Delete this card?')) return;
            
            try {
                await fetch(`/api/cards/${cardId}`, { method: 'DELETE' });
                await loadData();
            } catch (error) {
                console.error('Error deleting card:', error);
            }
        }
        
        // Column modal
        function openColumnModal() {
            document.getElementById('columnModal').classList.add('active');
            document.getElementById('columnTitle').value = '';
            document.getElementById('columnColor').value = '#e9e9e7';
            
            // Reset color selection
            document.querySelectorAll('.color-option').forEach(el => el.classList.remove('selected'));
            document.querySelector('.color-option').classList.add('selected');
            
            setTimeout(() => document.getElementById('columnTitle').focus(), 100);
        }
        
        function closeColumnModal() {
            document.getElementById('columnModal').classList.remove('active');
        }
        
        function selectColor(color) {
            document.getElementById('columnColor').value = color;
            document.querySelectorAll('.color-option').forEach(el => el.classList.remove('selected'));
            event.target.classList.add('selected');
        }
        
        async function saveColumn(event) {
            event.preventDefault();
            const title = document.getElementById('columnTitle').value;
            const color = document.getElementById('columnColor').value;
            
            try {
                await fetch('/api/columns', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ title, color })
                });
                
                closeColumnModal();
                await loadData();
            } catch (error) {
                console.error('Error creating column:', error);
                alert('Error creating column. Please try again.');
            }
        }
        
        async function deleteColumn(columnId) {
            if (!confirm('Delete this column and all its cards?')) return;
            
            try {
                await fetch(`/api/columns/${columnId}`, { method: 'DELETE' });
                await loadData();
            } catch (error) {
                console.error('Error deleting column:', error);
            }
        }
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            // ESC to close modals
            if (e.key === 'Escape') {
                closeCardModal();
                closeColumnModal();
            }
            // Ctrl/Cmd + K to add column
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                openColumnModal();
            }
        });
        
        // Initialize
        loadData();
        
        // Auto-refresh every 30 seconds
        setInterval(loadData, 30000);
    </script>
</body>
</html>
"""


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Advanced Kanban Board...")
    print("📍 Opening at: http://localhost:3000")
    print("✨ Features: Tags, Colors, Stats, Keyboard Shortcuts, Auto-refresh")
    uvicorn.run(app, host="0.0.0.0", port=3000)