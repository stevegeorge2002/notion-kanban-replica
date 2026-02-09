"""Modal components for creating/editing cards and columns."""
import reflex as rx


def card_modal(state) -> rx.Component:
    """Modal for creating/editing a card."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.dialog.title(
                        rx.cond(
                            state.modal_card_id,
                            "Edit Card",
                            "Create Card",
                        ),
                        font_size="18px",
                        font_weight="600",
                        color="#37352f",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="2",
                            padding="4px",
                        ),
                    ),
                    width="100%",
                    align_items="center",
                ),
                # Form
                rx.vstack(
                    # Title input
                    rx.vstack(
                        rx.text("Title", font_size="13px", font_weight="500", color="#37352f"),
                        rx.input(
                            value=state.modal_card_title,
                            on_change=state.set_modal_card_title,
                            placeholder="Enter card title...",
                            width="100%",
                            font_size="14px",
                        ),
                        spacing="1",
                        width="100%",
                        align_items="start",
                    ),
                    # Description input
                    rx.vstack(
                        rx.text("Description", font_size="13px", font_weight="500", color="#37352f"),
                        rx.text_area(
                            value=state.modal_card_description,
                            on_change=state.set_modal_card_description,
                            placeholder="Enter description (optional)...",
                            width="100%",
                            min_height="100px",
                            font_size="14px",
                        ),
                        spacing="1",
                        width="100%",
                        align_items="start",
                    ),
                    spacing="4",
                    width="100%",
                ),
                # Actions
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            on_click=state.close_card_modal,
                        ),
                    ),
                    rx.button(
                        "Save",
                        on_click=state.save_card,
                        color_scheme="blue",
                    ),
                    spacing="3",
                    width="100%",
                    justify="end",
                ),
                spacing="4",
                width="100%",
            ),
            max_width="500px",
            padding="24px",
            background_color="#ffffff",
            border_radius="8px",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.24)",
        ),
        open=state.show_card_modal,
    )


def column_modal(state) -> rx.Component:
    """Modal for creating a new column."""
    return rx.dialog.root(
        rx.dialog.content(
            rx.vstack(
                # Header
                rx.hstack(
                    rx.dialog.title(
                        "Create Column",
                        font_size="18px",
                        font_weight="600",
                        color="#37352f",
                    ),
                    rx.spacer(),
                    rx.dialog.close(
                        rx.button(
                            rx.icon("x", size=18),
                            variant="ghost",
                            size="2",
                            padding="4px",
                        ),
                    ),
                    width="100%",
                    align_items="center",
                ),
                # Form
                rx.vstack(
                    rx.text("Column Name", font_size="13px", font_weight="500", color="#37352f"),
                    rx.input(
                        value=state.new_column_title,
                        on_change=state.set_new_column_title,
                        placeholder="Enter column name...",
                        width="100%",
                        font_size="14px",
                    ),
                    spacing="1",
                    width="100%",
                    align_items="start",
                ),
                # Actions
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="soft",
                            color_scheme="gray",
                            on_click=state.close_column_modal,
                        ),
                    ),
                    rx.button(
                        "Create",
                        on_click=state.create_column,
                        color_scheme="blue",
                    ),
                    spacing="3",
                    width="100%",
                    justify="end",
                ),
                spacing="4",
                width="100%",
            ),
            max_width="400px",
            padding="24px",
            background_color="#ffffff",
            border_radius="8px",
            box_shadow="0 8px 32px rgba(0, 0, 0, 0.24)",
        ),
        open=state.show_column_modal,
    )
