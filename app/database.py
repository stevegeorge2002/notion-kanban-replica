"""Database configuration and initialization."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os

from .models import Base, BoardColumn, Card

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kanban.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Initialize database and create tables."""
    Base.metadata.create_all(bind=engine)
    
    # Add sample data if database is empty
    db = SessionLocal()
    try:
        if db.query(BoardColumn).count() == 0:
            # Create default columns
            columns = [
                BoardColumn(title="To Do", position=0, color="#e9e9e7"),
                BoardColumn(title="In Progress", position=1, color="#ffeaa7"),
                BoardColumn(title="Done", position=2, color="#81ecec"),
            ]
            db.add_all(columns)
            db.commit()
            
            # Create sample cards
            cards = [
                Card(title="Design Homepage", description="Create wireframes and mockups", column_id=1, position=0),
                Card(title="Setup Database", description="Configure PostgreSQL", column_id=1, position=1),
                Card(title="Build API", description="FastAPI endpoints", column_id=2, position=0),
                Card(title="Deploy to Production", description="Setup CI/CD", column_id=3, position=0),
            ]
            db.add_all(cards)
            db.commit()
    finally:
        db.close()


@contextmanager
def get_db() -> Session:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database initialized successfully!")
