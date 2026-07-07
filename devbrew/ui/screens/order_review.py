"""Order review and confirmation screen (DVBRW-11)."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Static

from devbrew.money import format_price


class OrderReviewScreen(Screen):
    """Review the order, then place it (persisting to the database)."""

    BINDINGS = [
        ("enter", "confirm", "Place order"),
        ("escape", "cancel", "Back"),
    ]

    def __init__(self) -> None:
        super().__init__()
        self._order = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical(id="review-frame"):
            yield Static("ORDER REVIEW", id="menu-title")
            yield Static(id="review-body")
            yield Static(id="review-status")
        yield Static("Enter place order   Esc back", id="menu-hint")
        yield Footer()

    def on_mount(self) -> None:
        self._render_review()

    def _render_review(self) -> None:
        cart = self.app.cart
        delivery = self.app.delivery
        lines = ["Items:"]
        for item in cart.items():
            lines.append(
                f"  {item.quantity} x {item.drink.item.name:<11} "
                f"{item.drink.descriptor:<26} {item.line_total_label:>10}"
            )
        lines.append("")
        lines.append(f"  {'Total':<39} {format_price(cart.total):>10}")
        lines.append("")
        lines.append("Deliver to:")
        if delivery is not None:
            lines.extend(f"  {line}" for line in delivery.summary_lines())
        self.query_one("#review-body", Static).update("\n".join(lines))

    def action_confirm(self) -> None:
        if self._order is not None:
            self.app.return_to_menu()
            return
        user = self.app.auth.current_user
        if user is None or self.app.cart.is_empty or self.app.delivery is None:
            self.app.notify("Nothing to place.", severity="warning")
            return

        order = self.app.orders.place_order(
            user=user, cart=self.app.cart, delivery=self.app.delivery
        )
        self._order = order
        self.app.delivery = None
        self.query_one("#review-status", Static).update(
            f"[green]✓ Order {order.id} placed![/]\n"
            f"Status: {order.status}\n"
            f"Press Enter to return to the menu."
        )
        self.query_one("#menu-hint", Static).update("Enter return to menu")

    def action_cancel(self) -> None:
        if self._order is not None:
            self.app.return_to_menu()
            return
        self.app.pop_screen()
