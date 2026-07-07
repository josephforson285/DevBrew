"""Shopping cart screen (DVBRW-9)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from devbrew.money import format_price
from devbrew.ui.widgets.cart_view import CartView


class CartScreen(Screen):
    """Review the cart: change quantities, remove items, see subtotal/total."""

    BINDINGS = [("escape", "app.pop_screen", "Back")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="cart-frame"):
            yield Static("YOUR CART", id="menu-title")
            yield CartView(self.app.cart, id="cart-view")
            yield Static(id="cart-summary")
        yield Static("↑/↓ select   +/- quantity   x remove   Esc back", id="menu-hint")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one(CartView).focus()
        self._refresh_summary()

    def _refresh_summary(self) -> None:
        cart = self.app.cart
        text = (
            f"Subtotal   {format_price(cart.subtotal)}\n"
            f"Total      {format_price(cart.total)}"
        )
        self.query_one("#cart-summary", Static).update(text)

    def on_cart_view_changed(self, event: CartView.Changed) -> None:
        self._refresh_summary()
