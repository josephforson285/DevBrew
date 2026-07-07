"""Cart list widget: navigate items, change quantity, remove (DVBRW-9)."""

from __future__ import annotations

from rich.text import Text
from textual import events
from textual.message import Message
from textual.reactive import reactive
from textual.widgets import Static

from devbrew.models.cart import Cart


class CartView(Static):
    """Shows cart lines with a '>' cursor; +/- change quantity, x removes."""

    can_focus = True
    index: reactive[int] = reactive(0)

    class Changed(Message):
        """Posted when the cart contents change."""

    def __init__(self, cart: Cart, **kwargs) -> None:
        super().__init__(**kwargs)
        self._cart = cart

    def on_mount(self) -> None:
        self._redraw()

    def _redraw(self) -> None:
        items = self._cart.items()
        out = Text()
        if not items:
            out.append("Your cart is empty.", style="dim")
            self.update(out)
            return
        for i, item in enumerate(items):
            selected = i == self.index
            out.append("> " if selected else "  ", style="bold #ff8c42" if selected else "")
            label = Text(f"{item.drink.item.name:<11} ({item.drink.descriptor})")
            if selected:
                label.stylize("bold")
            out.append_text(label)
            out.append(f"   x{item.quantity}   ", style="cyan")
            out.append(item.line_total_label, style="#ff8c42")
            if i < len(items) - 1:
                out.append("\n")
        self.update(out)

    def watch_index(self) -> None:
        self._redraw()

    def _clamp_index(self) -> None:
        count = len(self._cart.items())
        if count == 0:
            self.index = 0
        elif self.index >= count:
            self.index = count - 1

    def on_key(self, event: events.Key) -> None:
        items = self._cart.items()
        if not items:
            return
        key = event.key
        if key in ("up", "k"):
            event.stop()
            self.index = (self.index - 1) % len(items)
        elif key in ("down", "j"):
            event.stop()
            self.index = (self.index + 1) % len(items)
        elif key in ("right", "l", "plus"):
            event.stop()
            self._cart.update_quantity(self.index, items[self.index].quantity + 1)
            self._redraw()
            self.post_message(self.Changed())
        elif key in ("left", "h", "minus"):
            event.stop()
            self._cart.update_quantity(self.index, items[self.index].quantity - 1)
            self._clamp_index()
            self._redraw()
            self.post_message(self.Changed())
        elif key in ("x", "d", "delete"):
            event.stop()
            self._cart.remove(self.index)
            self._clamp_index()
            self._redraw()
            self.post_message(self.Changed())
