"""Coffee customization screen (DVBRW-8)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from devbrew.models.customization import (
    MILK_OPTIONS,
    SUGAR_LEVELS,
    Customization,
    CustomizedDrink,
)
from devbrew.models.menu import MenuItem
from devbrew.ui.logo import DEVBREW_ASCII
from devbrew.ui.widgets.option_picker import OptionPicker


class CustomizeScreen(Screen):
    """Choose size, milk, sugar, and extra shot; see a live order summary."""

    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def __init__(self, item: MenuItem) -> None:
        super().__init__()
        self._item = item

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(DEVBREW_ASCII.strip("\n"), id="logo")
        options = [
            ("Size", self._item.sizes),
            ("Milk", MILK_OPTIONS),
            ("Sugar", SUGAR_LEVELS),
            ("Extra shot", ("No", "Yes")),
        ]
        with Vertical(id="customize-frame"):
            yield Static(f"CUSTOMIZE  ·  {self._item.name}", id="menu-title")
            yield OptionPicker(options, id="option-picker")
            yield Static("ORDER SUMMARY", id="summary-title")
            yield Static(id="summary")
        yield Static("↑/↓ field   ←/→ change   Enter confirm   Esc back", id="menu-hint")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(OptionPicker).focus()
        self._refresh_summary()

    def _current_drink(self) -> CustomizedDrink:
        choices = self.query_one(OptionPicker).choices
        customization = Customization(
            size=choices["Size"],
            milk=choices["Milk"],
            sugar=choices["Sugar"],
            extra_shot=choices["Extra shot"] == "Yes",
        )
        return CustomizedDrink(self._item, customization)

    def _refresh_summary(self) -> None:
        drink = self._current_drink()
        self.query_one("#summary", Static).update("\n".join(drink.summary_lines()))

    def on_option_picker_changed(self, event: OptionPicker.Changed) -> None:
        self._refresh_summary()

    def on_option_picker_confirmed(self, event: OptionPicker.Confirmed) -> None:
        drink = self._current_drink()
        self.app.cart.add(drink)
        self.app.notify(
            f"Added {drink.item.name} to cart ({drink.price_label}). Press 'c' to view cart.",
            title="Cart",
        )
        self.app.pop_screen()
