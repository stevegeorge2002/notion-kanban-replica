"""State management for Kanban board application."""
import reflex as rx
from typing import List, Optional
import httpx


class State(rx.State):
    """State for the Kanban board."""
    
    # Data
    columns: List[dict] = []
    cards: List[dict] = []
    
    # UI State
    is_loading: bool = True
    show_card_modal: bool = False
    show_column_modal: bool = False
    
    # Modal data
    modal_card_id: Optional[int] = None
    modal_card_title: str = ""
    modal_card_description: str = ""
    modal_card_column_id: Optional[int] = None
    
    # New column
    new_column_title: str = ""
    
    # Drag and drop
    dragging_card_id: Optional[int] = None
    drag_over_column_id: Optional[int] = None
    
    API_BASE = "http://localhost:8000/api"
    
    async def load_data(self):
        """Load columns and cards from API."""
        self.is_loading = True
        try:
            async with httpx.AsyncClient() as client:
                # Load columns
                columns_response = await client.get(f"{self.API_BASE}/columns")
                self.columns = columns_response.json()
                
                # Load cards
                cards_response = await client.get(f"{self.API_BASE}/cards")
                self.cards = cards_response.json()
        except Exception as e:
            print(f"Error loading data: {e}")
        finally:
            self.is_loading = False
    
    def get_cards_for_column(self, column_id: int) -> List[dict]:
        """Get all cards for a specific column."""
        return [card for card in self.cards if card["column_id"] == column_id]
    
    # Card operations
    def open_card_modal(self, card_id: Optional[int] = None, column_id: Optional[int] = None):
        """Open modal to create or edit card."""
        if card_id:
            # Edit existing card
            card = next((c for c in self.cards if c["id"] == card_id), None)
            if card:
                self.modal_card_id = card_id
                self.modal_card_title = card["title"]
                self.modal_card_description = card.get("description", "")
                self.modal_card_column_id = card["column_id"]
        else:
            # Create new card
            self.modal_card_id = None
            self.modal_card_title = ""
            self.modal_card_description = ""
            self.modal_card_column_id = column_id
        
        self.show_card_modal = True
    
    def close_card_modal(self):
        """Close card modal."""
        self.show_card_modal = False
        self.modal_card_id = None
        self.modal_card_title = ""
        self.modal_card_description = ""
        self.modal_card_column_id = None
    
    async def save_card(self):
        """Save card (create or update)."""
        if not self.modal_card_title.strip():
            return
        
        async with httpx.AsyncClient() as client:
            try:
                if self.modal_card_id:
                    # Update existing card
                    await client.put(
                        f"{self.API_BASE}/cards/{self.modal_card_id}",
                        json={
                            "title": self.modal_card_title,
                            "description": self.modal_card_description,
                        }
                    )
                else:
                    # Create new card
                    await client.post(
                        f"{self.API_BASE}/cards",
                        json={
                            "title": self.modal_card_title,
                            "description": self.modal_card_description,
                            "column_id": self.modal_card_column_id,
                        }
                    )
                
                # Reload data
                await self.load_data()
                self.close_card_modal()
            except Exception as e:
                print(f"Error saving card: {e}")
    
    async def delete_card(self, card_id: int):
        """Delete a card."""
        async with httpx.AsyncClient() as client:
            try:
                await client.delete(f"{self.API_BASE}/cards/{card_id}")
                await self.load_data()
            except Exception as e:
                print(f"Error deleting card: {e}")
    
    # Column operations
    def open_column_modal(self):
        """Open modal to create column."""
        self.new_column_title = ""
        self.show_column_modal = True
    
    def close_column_modal(self):
        """Close column modal."""
        self.show_column_modal = False
        self.new_column_title = ""
    
    async def create_column(self):
        """Create a new column."""
        if not self.new_column_title.strip():
            return
        
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    f"{self.API_BASE}/columns",
                    json={"title": self.new_column_title}
                )
                await self.load_data()
                self.close_column_modal()
            except Exception as e:
                print(f"Error creating column: {e}")
    
    async def delete_column(self, column_id: int):
        """Delete a column."""
        async with httpx.AsyncClient() as client:
            try:
                await client.delete(f"{self.API_BASE}/columns/{column_id}")
                await self.load_data()
            except Exception as e:
                print(f"Error deleting column: {e}")
    
    # Drag and drop
    def on_drag_start(self, card_id: int):
        """Handle drag start."""
        self.dragging_card_id = card_id
    
    def on_drag_over(self, column_id: int):
        """Handle drag over column."""
        self.drag_over_column_id = column_id
    
    async def on_drop(self, column_id: int, position: int = 0):
        """Handle card drop."""
        if not self.dragging_card_id:
            return
        
        async with httpx.AsyncClient() as client:
            try:
                await client.patch(
                    f"{self.API_BASE}/cards/{self.dragging_card_id}/move",
                    json={
                        "column_id": column_id,
                        "position": position
                    }
                )
                await self.load_data()
            except Exception as e:
                print(f"Error moving card: {e}")
            finally:
                self.dragging_card_id = None
                self.drag_over_column_id = None
