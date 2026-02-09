"""Card component for Kanban board."""
import reflex as rx
from typing import Dict


def card_component(card: Dict, state) -> rx.Component:
    """Render a single card."""
    return rx.box(
        # Card content
        rx.vstack(
            # Title
            rx.text(
                card["title"],
                font_size="14px",
                font_weight="500",
                color="#37352f",
                line_height="1.5",
            ),
            # Description (if exists)
            rx.cond(
                card.get("description"),
                rx.text(
                    card.get("description", ""),
                    font_size="12px",
                    color="#787774",
                    line_height="1.4",
                    margin_top="4px",
                ),
            ),
            # Actions (appear on hover)
            rx.hstack(
                rx.button(
                    "Edit",
                    on_click=lambda: state.open_card_modal(card["id"]),
                    size="1",
                    variant="ghost",
                    color_scheme="gray",
                    font_size="11px",
                    padding="4px 8px",
                    height="24px",
                    class_name="card-action-btn",
                ),
                rx.button(
                    "Delete",
                    on_click=lambda: state.delete_card(card["id"]),
                    size="1",
                    variant="ghost",
                    color_scheme="red",
                    font_size="11px",
                    padding="4px 8px",
                    height="24px",
                    class_name="card-action-btn",
                ),
                spacing="2",
                margin_top="8px",
                opacity="0",
                class_name="card-actions",
            ),
            align_items="start",
            spacing="0",
            width="100%",
        ),
        # Card styling
        background_color="#ffffff",
        border_radius="3px",
        padding="12px",
        border=f"1px solid #e3e2e0",
        box_shadow="0 1px 3px rgba(0, 0, 0, 0.12)",
        cursor="grab",
        transition="all 0.2s",
        width="100%",
        margin_bottom="8px",
        draggable="true",
        on_drag_start=lambda: state.on_drag_start(card["id"]),
        _hover={
            "box_shadow": "0 2px 8px rgba(0, 0, 0, 0.15)",
            "border_color": "#d3d2d0",
        },
        class_name="kanban-card",
        position="relative",
    )
