"""Main Reflex application."""
import reflex as rx
from .state import State


def index() -> rx.Component:
    """Main page."""
    return rx.container(
        rx.heading("Kanban Board", size="9"),
        rx.text("Reflex + FastAPI Full Stack"),
        rx.text(f"Loading: {State.is_loading}"),
        rx.button("Load Data", on_click=State.load_data),
        padding="2em",
    )


# Create app
app = rx.App()

# Add page
app.add_page(
    index,
    route="/",
    title="Notion Kanban Board",
    on_load=State.load_data,
)