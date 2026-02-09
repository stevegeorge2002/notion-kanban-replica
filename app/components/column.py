"""Column component for Kanban board."""
import reflex as rx
from typing import Dict, List
from .card import card_component


def column_component(column: Dict, cards: List[Dict], state) -> rx.Component:
    """Render a single column with its cards."""
    return rx.box(
        rx.vstack(
            # Column header
            rx.hstack(
                rx.text(
                    column["title"],
                    font_size="14px",
                    font_weight="600",
                    color="#37352f",
                ),
                rx.spacer(),
                rx.hstack(
                    rx.text(
                        str(len(cards)),
                        font_size="12px",
                        color="#787774",
                    ),
                    rx.button(
                        rx.icon("plus", size=14),
                        on_click=lambda: state.open_card_modal(column_id=column["id"]),
                        size="1",
                        variant="ghost",
                        color_scheme="gray",
                        padding="4px",
                        height="24px",
                        width="24px",
                        class_name="column-add-btn",
                    ),
                    rx.button(
                        rx.icon("trash-2", size=14),
                        on_click=lambda: state.delete_column(column["id"]),
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        padding="4px",
                        height="24px",
                        width="24px",
                        class_name="column-delete-btn",
                    ),
                    spacing="1",
                ),
                width="100%",
                align_items="center",
                padding="12px 16px",
                background_color=column.get("color", "#e9e9e7"),
                border_radius="6px 6px 0 0",
            ),
            # Cards container
            rx.box(
                rx.foreach(
                    cards,
                    lambda card: card_component(card, state),
                ),
                # Empty state
                rx.cond(
                    len(cards) == 0,
                    rx.text(
                        "Drop cards here",
                        font_size="12px",
                        color="#9b9a97",
                        text_align="center",
                        padding="24px",
                    ),
                ),
                padding="16px",
                min_height="200px",
                width="100%",
                on_drag_over=lambda e: e.prevent_default(),
                on_drop=lambda: state.on_drop(column["id"], 0),
            ),
            spacing="0",
            width="100%",
            height="100%",
        ),
        # Column styling
        background_color="#f7f6f3",
        border_radius="6px",
        border="1px solid #e3e2e0",
        min_width="280px",
        max_width="320px",
        height="fit-content",
        flex_shrink="0",
        class_name="kanban-column",
    )
