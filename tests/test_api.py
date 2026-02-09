"""Test suite for Kanban API."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api import app, get_db_session
from app.models import Base
from app.database import init_db

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db_session] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_database():
    """Setup test database before each test."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_create_column():
    """Test column creation."""
    response = client.post("/api/columns", json={"title": "Test Column"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Column"
    assert "id" in data


def test_get_columns():
    """Test getting all columns."""
    # Create test column
    client.post("/api/columns", json={"title": "Column 1"})
    client.post("/api/columns", json={"title": "Column 2"})
    
    # Get columns
    response = client.get("/api/columns")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_create_card():
    """Test card creation."""
    # Create column first
    col_response = client.post("/api/columns", json={"title": "Test Column"})
    column_id = col_response.json()["id"]
    
    # Create card
    response = client.post("/api/cards", json={
        "title": "Test Card",
        "description": "Test Description",
        "column_id": column_id
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Card"
    assert data["column_id"] == column_id


def test_update_card():
    """Test card update."""
    # Setup
    col_response = client.post("/api/columns", json={"title": "Test Column"})
    column_id = col_response.json()["id"]
    card_response = client.post("/api/cards", json={
        "title": "Original Title",
        "column_id": column_id
    })
    card_id = card_response.json()["id"]
    
    # Update card
    response = client.put(f"/api/cards/{card_id}", json={
        "title": "Updated Title",
        "description": "New Description"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "New Description"


def test_delete_card():
    """Test card deletion."""
    # Setup
    col_response = client.post("/api/columns", json={"title": "Test Column"})
    column_id = col_response.json()["id"]
    card_response = client.post("/api/cards", json={
        "title": "Test Card",
        "column_id": column_id
    })
    card_id = card_response.json()["id"]
    
    # Delete card
    response = client.delete(f"/api/cards/{card_id}")
    assert response.status_code == 200
    
    # Verify deletion
    get_response = client.get("/api/cards")
    assert len(get_response.json()) == 0


def test_move_card():
    """Test moving card between columns."""
    # Setup
    col1_response = client.post("/api/columns", json={"title": "Column 1"})
    col2_response = client.post("/api/columns", json={"title": "Column 2"})
    column1_id = col1_response.json()["id"]
    column2_id = col2_response.json()["id"]
    
    card_response = client.post("/api/cards", json={
        "title": "Test Card",
        "column_id": column1_id
    })
    card_id = card_response.json()["id"]
    
    # Move card
    response = client.patch(f"/api/cards/{card_id}/move", json={
        "column_id": column2_id,
        "position": 0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["column_id"] == column2_id


def test_delete_column_cascade():
    """Test that deleting column deletes its cards."""
    # Setup
    col_response = client.post("/api/columns", json={"title": "Test Column"})
    column_id = col_response.json()["id"]
    client.post("/api/cards", json={"title": "Card 1", "column_id": column_id})
    client.post("/api/cards", json={"title": "Card 2", "column_id": column_id})
    
    # Delete column
    response = client.delete(f"/api/columns/{column_id}")
    assert response.status_code == 200
    
    # Verify cards are deleted
    cards_response = client.get("/api/cards")
    assert len(cards_response.json()) == 0
