"""Main Kanban board component."""
import reflex as rx
from .column import column_component
from .modal import card_modal, column_modal


def board_component(state) -> rx.Component:
    """Render the complete Kanban board."""
    return rx.box(
        # Header
        rx.vstack(
            rx.hstack(
                rx.heading(
                    "Kanban Board",
                    font_size="28px",
                    font_weight="700",
                    color="#37352f",
                ),
                rx.spacer(),
                rx.button(
                    rx.icon("plus", size=16),
                    "Add Column",
                    on_click=state.open_column_modal,
                    color_scheme="blue",
                    size="2",
                ),
                width="100%",
                align_items="center",
                padding="24px 32px",
            ),
            # Board container
            rx.cond(
                state.is_loading,
                # Loading state
                rx.center(
                    rx.spinner(size="3"),
                    padding="64px",
                ),
                # Board with columns
                rx.box(
                    rx.hstack(
                        rx.foreach(
                            state.columns,
                            lambda col: column_component(
                                col,
                                state.get_cards_for_column(col["id"]),
                                state,
                            ),
                        ),
                        spacing="4",
                        align_items="start",
                        overflow_x="auto",
                        padding="0 32px 32px",
                    ),
                    width="100%",
                ),
            ),
            spacing="0",
            width="100%",
            height="100vh",
        ),
        # Modals
        card_modal(state),
        column_modal(state),
        # Page styling
        background_color="#ffffff",
        width="100%",
        height="100vh",
        overflow="hidden",
    )
