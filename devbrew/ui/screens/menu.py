"""Coffee menu screen: classic arrow-key list with a '>' cursor (DVBRW-7)."""

from __future__ import annotations

from rich.text import Text
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from devbrew.models.menu import MenuItem
from devbrew.ui.logo import DEVBREW_ASCII
from devbrew.ui.widgets.arrow_menu import ArrowMenu

# Column widths for aligned rows: number, name, description, sizes, price.
_HEADER = f"  {'#':<2} {'Name':<11} {'Description':<24} {'Sizes':<9}  {'Price':>10}"


def _row(index: int, item: MenuItem) -> Text:
    row = Text()
    row.append(f"{index:<2} ", style="dim")
    row.append(f"{item.name:<11} ")
    row.append(f"{item.description:<24} ", style="dim")
    row.append(f"{item.sizes_label:<9}  ", style="dim")
    row.append(f"{item.price_label:>10}", style="#ff8c42")
    return row


class MenuScreen(Screen):
    """Browse the coffee menu with the arrow keys; Esc returns to the console."""

    BINDINGS = [
        ("c", "view_cart", "Cart"),
        ("escape", "app.pop_screen", "Back"),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(DEVBREW_ASCII.strip("\n"), id="logo")
        yield Static(self._greeting(), id="greeting")
        self._items = self.app.menu.list_items()
        rows = [_row(i, item) for i, item in enumerate(self._items, start=1)]
        with Vertical(id="menu-frame"):
            yield Static("COFFEE MENU", id="menu-title")
            yield Static(_HEADER, id="menu-head")
            yield ArrowMenu(rows, id="menu-list")
        yield Static("↑/↓ navigate   Enter customize   c cart   Esc back", id="menu-hint")
        yield Footer()

    def action_view_cart(self) -> None:
        self.app.show_cart()

    def _greeting(self) -> str:
        user = self.app.auth.current_user
        name = user.name if user else "there"
        return f"Hi, {name} — ready for a coffee?"

    def on_mount(self) -> None:
        self.query_one(ArrowMenu).focus()

    def on_arrow_menu_selected(self, event: ArrowMenu.Selected) -> None:
        from devbrew.ui.screens.customize import CustomizeScreen

        item = self._items[event.index]
        self.app.push_screen(CustomizeScreen(item))
