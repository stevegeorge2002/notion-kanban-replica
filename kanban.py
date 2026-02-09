"""Working Reflex Kanban Board."""
import reflex as rx


class State(rx.State):
    """Simple state for demo."""
    message: str = "Kanban Board - Reflex Version"


def index() -> rx.Component:
    """Main page."""
    return rx.container(
        rx.heading(State.message, size="9"),
        rx.text("This is a working Reflex app!"),
        rx.text("The full Kanban functionality requires FastAPI backend."),
        rx.button("Test Button", on_click=State.set_message("Button clicked!")),
    )


app = rx.App()
app.add_page(index)